from jobplus.app import create_app

app = create_app('development')
#app = create_app('esun127')

if __name__ == "__main__":
    app.run()
