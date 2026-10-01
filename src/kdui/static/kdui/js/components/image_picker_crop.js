/* KD UI Image Picker — crop/resize + photo search add-on.

   Ported from MiniPass's photo-normalizer.js (the organization logo picker). The logic
   is the same: a chosen file opens a crop dialog, the crop is resized and compressed in
   the browser, and the result replaces the file in the form; a search opens a grid of
   results and the picked photo is downloaded by the server. What changed: Bootstrap
   modals are native <dialog> elements, and the picker's own preview, remove button and
   file checks are used (initKduiImagePicker) instead of a second copy.

   Needs Cropper.js (window.Cropper) for the crop step, and the dialogs from
   image_picker_dialogs() in kdui/components/image_picker.html.

   initKduiImageCrop({
     id,                    // the image_picker id
     aspectRatio: NaN,      // 1 for a square crop, NaN for free
     maxWidth: 1200, maxHeight: 800, quality: 0.92, outputFormat: 'image/jpeg',
     searchUrl,             // GET ?q=&page= -> [{id?, thumb, full, alt?}]  (optional: no search without it)
     downloadUrl,           // GET ?url=&id= -> {success, filename}   (id: the result's id, if it has one)
     imageBaseUrl,          // filename -> preview URL: imageBaseUrl + filename
   })
*/
(() => {
  function initKduiImageCrop(config = {}) {
    const opts = {
      aspectRatio: NaN, maxWidth: 1200, maxHeight: 800, quality: 0.92, outputFormat: 'image/jpeg',
      searchUrl: null, downloadUrl: null, imageBaseUrl: '', ...config,
    };
    const id = opts.id;
    const root = document.querySelector(`[data-kdui-image-picker="${CSS.escape(id || '')}"]`);
    if (!root || !window.initKduiImagePicker) return null;

    const byId = (suffix) => document.getElementById(`${id}-${suffix}`);
    const upload = byId('upload');
    const hidden = byId('selected');
    const cropDialog = byId('crop');
    const cropImage = byId('crop-image');
    const cropConfirm = byId('crop-confirm');
    const cropCancel = byId('crop-cancel');
    const resultsDialog = byId('results');
    const resultsGrid = byId('results-grid');
    const prevButton = byId('results-prev');
    const nextButton = byId('results-next');

    let cropper = null;
    let confirmed = false;
    let page = 1;
    let query = '';
    const current = () => root.querySelector('.kdui-image-picker__image');
    // What the picker showed before a new file was chosen, so Cancel can put it back.
    let saved = { src: current()?.src || null, alt: current()?.alt || '', value: hidden?.value || '' };
    let savedFile = null; // the cropped file already in the form, if any

    const picker = window.initKduiImagePicker({
      id,
      onSearch: opts.searchUrl && resultsDialog ? (text, controller) => search(text, controller) : undefined,
    });

    root.addEventListener('kdui:image-remove', () => { savedFile = null; saved = { src: null, alt: '', value: '' }; });

    // ── File selected → open the crop dialog ─────────────────────────────────
    function startCropper() {
      if (cropper) cropper.destroy();
      cropper = new Cropper(cropImage, {
        aspectRatio: opts.aspectRatio, viewMode: 1, autoCropArea: 0.9,
        movable: true, zoomable: true, rotatable: false, scalable: false, responsive: true,
      });
    }

    root.addEventListener('kdui:image-select', (event) => {
      if (!cropDialog || !cropImage || !window.Cropper) return; // no cropper: the picked file is used as is
      confirmed = false;
      cropImage.onload = () => { cropImage.onload = null; startCropper(); };
      cropImage.src = event.detail.url;
      cropDialog.showModal();
    });

    // ── Confirm crop: resize + compress → put in the file input → update the preview ──
    cropConfirm?.addEventListener('click', () => {
      if (!cropper) return;
      const format = opts.outputFormat;
      const extension = format === 'image/png' ? 'png' : 'jpg';
      cropper.getCroppedCanvas({
        maxWidth: opts.maxWidth, maxHeight: opts.maxHeight, imageSmoothingQuality: 'high',
      }).toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        const file = new File([blob], `photo.${extension}`, { type: format });
        const files = new DataTransfer();
        files.items.add(file);
        if (upload) upload.files = files.files;
        savedFile = file;
        picker.setImage(url, 'Selected image preview', '');
        saved = { src: url, alt: 'Selected image preview', value: '' };
        confirmed = true;
        cropDialog.close();
      }, format, format === 'image/png' ? undefined : opts.quality);
    });

    cropCancel?.addEventListener('click', () => cropDialog.close());
    cropDialog?.addEventListener('close', () => {
      if (cropper) { cropper.destroy(); cropper = null; }
      if (confirmed) return;
      // Cancelled (button or Escape): forget the chosen file and show what was there before.
      if (upload) {
        upload.value = '';
        if (savedFile) {
          const files = new DataTransfer();
          files.items.add(savedFile);
          upload.files = files.files;
        }
      }
      if (saved.src) picker.setImage(saved.src, saved.alt, saved.value);
      else { picker.reset(false); picker.setStatus(''); }
    });

    // ── Search: results grid → the server downloads the picked photo ─────────
    const message = (text) => {
      resultsGrid.replaceChildren();
      const note = document.createElement('p');
      note.className = 'kdui-image-results__message';
      note.textContent = text;
      resultsGrid.append(note);
      prevButton.disabled = true;
      nextButton.disabled = true;
    };

    async function load(pageNumber) {
      message('Loading…');
      let response;
      try {
        response = await fetch(`${opts.searchUrl}?q=${encodeURIComponent(query)}&page=${pageNumber}`, { headers: { Accept: 'application/json' } });
      } catch (_) {
        message('Image search service is temporarily unavailable. Try again later, or upload your own image.');
        return false;
      }
      const data = await response.json().catch(() => null);
      if (!response.ok || !Array.isArray(data)) {
        let text = (data && data.error) || 'Search failed. Try again, or upload your own image.';
        if (text.includes('API key')) text = 'Image search is not available. The API key needs to be configured by an administrator.';
        message(text);
        return false;
      }
      if (!data.length) {
        message('No images found for this search.');
        prevButton.disabled = pageNumber === 1;
        return true;
      }
      resultsGrid.replaceChildren(...data.map((image) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'kdui-image-results__item';
        const thumb = document.createElement('img');
        thumb.src = image.thumb;
        thumb.alt = image.alt || 'Search result';
        thumb.loading = 'lazy';
        button.append(thumb);
        button.addEventListener('click', () => choose(image, button));
        return button;
      }));
      prevButton.disabled = pageNumber === 1;
      nextButton.disabled = false;
      return true;
    }

    async function choose(image, button) {
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
      try {
        const response = await fetch(`${opts.downloadUrl}?url=${encodeURIComponent(image.full)}&id=${encodeURIComponent(image.id || '')}`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error || 'download failed');
        if (upload) upload.value = '';
        savedFile = null;
        picker.setImage(opts.imageBaseUrl + result.filename, image.alt || 'Selected image preview', result.filename);
        saved = { src: opts.imageBaseUrl + result.filename, alt: image.alt || '', value: result.filename };
        resultsDialog.close();
        picker.setStatus('Photo selected.', 'success');
      } catch (_) {
        button.disabled = false;
        button.removeAttribute('aria-busy');
        picker.setStatus('That photo could not be downloaded. Choose another one.', 'error');
      }
    }

    async function search(text) {
      query = text;
      page = 1;
      resultsDialog.showModal();
      await load(1);
      picker.setStatus('');
    }

    prevButton?.addEventListener('click', () => { if (page > 1) { page -= 1; load(page); } });
    nextButton?.addEventListener('click', () => { page += 1; load(page); });
    resultsDialog?.addEventListener('click', (event) => { if (event.target === resultsDialog) resultsDialog.close(); });

    return picker;
  }

  window.initKduiImageCrop = initKduiImageCrop;
})();
