/* KD UI Image Picker — responsive search/upload interaction. */
(() => {
  const instances = new WeakMap();

  function createPlaceholder(label) {
    const wrapper = document.createElement('span');
    wrapper.className = 'kdui-image-picker__placeholder';
    wrapper.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>';
    const text = document.createElement('span');
    text.textContent = label;
    wrapper.append(text);
    return wrapper;
  }

  function initialize(root, suppliedOptions = {}) {
    if (!root) return null;
    if (instances.has(root)) {
      const existing = instances.get(root);
      Object.assign(existing.options, suppliedOptions);
      return existing.controller;
    }

    const options = { ...suppliedOptions };
    const id = root.dataset.kduiImagePicker;
    const byId = (suffix) => root.querySelector(`#${CSS.escape(id)}-${suffix}`);
    const trigger = byId('preview');
    const panel = byId('options');
    const modeTabs = [...root.querySelectorAll('[data-kdui-image-mode]')];
    const searchPanel = byId('search-panel');
    const uploadPanel = byId('upload-panel');
    const upload = byId('upload');
    const search = byId('search');
    const searchButton = byId('search-button');
    const hidden = root.parentElement.querySelector(`#${CSS.escape(id)}-selected`);
    const status = root.parentElement.querySelector(`#${CSS.escape(id)}-status`);
    const placeholderLabel = options.placeholderLabel || root.dataset.placeholderLabel || 'Add photo';
    const maxSizeMb = Number(root.dataset.maxSizeMb) || 5;
    const acceptedTypes = (root.dataset.accept || 'image/png,image/jpeg,image/webp')
      .split(',').map((value) => value.trim().toLowerCase()).filter(Boolean);
    let ownedObjectUrl = null;

    const setStatus = (message = '', variant = '') => {
      if (!status) return;
      status.textContent = message;
      if (variant) status.dataset.variant = variant;
      else delete status.dataset.variant;
    };

    const setLoading = (loading) => {
      if (!searchButton) return;
      searchButton.disabled = loading;
      searchButton.setAttribute('aria-busy', String(loading));
      root.toggleAttribute('data-searching', loading);
    };

    const setPanel = (open, restoreFocus = false) => {
      if (!panel || !trigger) return;
      panel.hidden = !open;
      root.toggleAttribute('data-open', open);
      trigger.setAttribute('aria-expanded', String(open));
      if (!open && restoreFocus) trigger.focus();
    };

    const selectMode = (mode, moveFocus = false) => {
      const selectedMode = mode === 'upload' ? 'upload' : 'search';
      root.dataset.mode = selectedMode;
      modeTabs.forEach((tab) => {
        const selected = tab.dataset.kduiImageMode === selectedMode;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        if (selected && moveFocus) tab.focus();
      });
      if (searchPanel) searchPanel.hidden = selectedMode !== 'search';
      if (uploadPanel) uploadPanel.hidden = selectedMode !== 'upload';
      setStatus('');
    };

    const ensureRemoveButton = () => {
      let remove = root.querySelector('[data-kdui-image-delete]');
      if (remove) return remove;
      remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'btn kdui-image-picker__remove';
      remove.dataset.variant = 'destructive';
      remove.dataset.size = 'icon-xs';
      remove.dataset.kduiImageDelete = '';
      remove.setAttribute('aria-label', 'Remove photo');
      remove.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>';
      trigger.after(remove);
      return remove;
    };

    const releaseObjectUrl = () => {
      if (!ownedObjectUrl) return;
      URL.revokeObjectURL(ownedObjectUrl);
      ownedObjectUrl = null;
    };

    const setImage = (src, alt = 'Selected image preview', selectedValue = '') => {
      if (!trigger) return;
      if (ownedObjectUrl && src !== ownedObjectUrl) releaseObjectUrl();
      const image = document.createElement('img');
      image.src = src;
      image.alt = alt;
      image.width = 100;
      image.height = 100;
      image.loading = 'lazy';
      image.decoding = 'async';
      image.className = 'kdui-image-picker__image';
      image.addEventListener('error', () => setStatus('The image could not be displayed. Choose another image.', 'error'), { once: true });
      trigger.replaceChildren(image);
      trigger.setAttribute('aria-label', 'Change photo');
      if (hidden) hidden.value = selectedValue;
      ensureRemoveButton();
      setPanel(false, true);
    };

    const reset = (restoreFocus = true) => {
      if (!trigger) return;
      releaseObjectUrl();
      trigger.replaceChildren(createPlaceholder(placeholderLabel));
      trigger.setAttribute('aria-label', placeholderLabel);
      root.querySelector('[data-kdui-image-delete]')?.remove();
      if (hidden) hidden.value = '';
      if (upload) upload.value = '';
      setStatus('Photo removed.');
      setPanel(false, restoreFocus);
      options.onDelete?.();
      root.dispatchEvent(new CustomEvent('kdui:image-remove', { bubbles: true }));
    };

    const controller = {
      setImage,
      reset,
      setStatus,
      setLoading,
      selectMode,
      open: () => setPanel(true),
      close: () => setPanel(false, true),
    };
    instances.set(root, { controller, options });

    trigger?.addEventListener('click', () => setPanel(panel?.hidden ?? false));
    root.addEventListener('click', (event) => {
      if (event.target.closest('[data-kdui-image-delete]')) {
        event.stopPropagation();
        reset(true);
      }
    });
    root.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && panel && !panel.hidden) {
        event.preventDefault();
        setPanel(false, true);
      }
    });
    document.addEventListener('pointerdown', (event) => {
      if (panel && !panel.hidden && !root.contains(event.target)) setPanel(false);
    });

    modeTabs.forEach((tab, index) => {
      tab.addEventListener('click', () => selectMode(tab.dataset.kduiImageMode));
      tab.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let next = index;
        if (event.key === 'ArrowLeft') next = (index - 1 + modeTabs.length) % modeTabs.length;
        if (event.key === 'ArrowRight') next = (index + 1) % modeTabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = modeTabs.length - 1;
        selectMode(modeTabs[next].dataset.kduiImageMode, true);
      });
    });
    selectMode(root.dataset.mode);

    upload?.addEventListener('change', async () => {
      const file = upload.files?.[0];
      if (!file) return;
      const extension = `.${file.name.split('.').pop()?.toLowerCase()}`;
      const accepted = acceptedTypes.some((type) =>
        type === file.type.toLowerCase() ||
        (type.endsWith('/*') && file.type.toLowerCase().startsWith(type.slice(0, -1))) ||
        (type.startsWith('.') && type === extension)
      );
      if (!file.type.startsWith('image/') || !accepted) {
        upload.value = '';
        setStatus('Choose a supported image file such as PNG, JPEG, or WebP.', 'error');
        return;
      }
      if (file.size > maxSizeMb * 1024 * 1024) {
        upload.value = '';
        setStatus(`Choose an image smaller than ${maxSizeMb} MB.`, 'error');
        return;
      }

      const url = URL.createObjectURL(file);
      const probe = new Image();
      probe.src = url;
      try {
        await probe.decode();
      } catch (_) {
        URL.revokeObjectURL(url);
        upload.value = '';
        setStatus('This image could not be read. Choose another file.', 'error');
        return;
      }

      releaseObjectUrl();
      ownedObjectUrl = url;
      if (hidden) hidden.value = '';
      setImage(url, 'Selected image preview');
      setStatus('Photo selected.', 'success');
      options.onSelect?.(file, url);
      root.dispatchEvent(new CustomEvent('kdui:image-select', { bubbles: true, detail: { file, url } }));
    });

    const submitSearch = async () => {
      const query = search?.value.trim() || '';
      if (!query) {
        setStatus('Enter a search term.', 'error');
        search?.focus();
        return;
      }

      setLoading(true);
      setStatus('Searching…');
      try {
        if (options.onSearch) {
          await options.onSearch(query, controller);
        } else {
          const event = new CustomEvent('kdui:image-search', {
            bubbles: true,
            cancelable: true,
            detail: { query, ...controller },
          });
          const handled = !root.dispatchEvent(event);
          if (!handled) setStatus('Image search is not configured. Use Upload instead.', 'error');
        }
      } catch (_) {
        setStatus('Image search failed. Try again or upload a photo.', 'error');
      } finally {
        setLoading(false);
      }
    };
    searchButton?.addEventListener('click', submitSearch);
    search?.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        submitSearch();
      }
    });

    return controller;
  }

  function init(config = {}) {
    const root = config.root || document.querySelector(`[data-kdui-image-picker="${CSS.escape(config.id || '')}"]`);
    return initialize(root, config);
  }

  function refresh() {
    document.querySelectorAll('[data-kdui-image-picker]').forEach((root) => initialize(root));
  }

  window.initKduiImagePicker = init;
  window.kduiImagePicker = { refresh };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refresh);
  else refresh();
})();
