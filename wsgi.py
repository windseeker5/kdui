import argparse

from app import create_app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask development server.")
    parser.add_argument("--host", default="127.0.0.1", help="Address to listen on. Use 0.0.0.0 for your local network.")
    parser.add_argument("--port", type=int, required=True, help="Port to listen on, for example 5005.")
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port)
