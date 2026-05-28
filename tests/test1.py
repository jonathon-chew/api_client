from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def main():
    print(f"{request.headers=}")
    print(f"{request.get_data(as_text=True)=}")
    return "Hello World"

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)