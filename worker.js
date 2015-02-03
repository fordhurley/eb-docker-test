function greet() {
    msg = process.env.GREETING + ', ' + process.env.NAME + ' at ' + Date.now()
    console.log(msg);
    setTimeout(greet, 5000);
}

greet()
