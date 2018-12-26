from demo import create_app

# Create flask app
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
