from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Welcome to the SSTI Demo</h1>
    <form method="POST" action="/greet">
        <label for="name">Enter your name:</label>
        <input type="text" id="name" name="name" />
        <label for="message">Enter your message:</label>
        <input type="text" id="message" name="message" />
        <input type="submit" value="Greet Me!" />
    </form>
    '''

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    message = request.form['message']
    
    # Create a vulnerable template
    template = f'''
    <h2>Hello, {name}!</h2>
    <p>Your message: {message}</p>
    '''
    
    # Render the template with the `message` variable
    return render_template_string(template, message=message)

if __name__ == '__main__':
    app.run(debug=True)
