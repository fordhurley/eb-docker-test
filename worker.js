function sayHi() {
    console.log('hi at', Date.now());
    setTimeout(sayHi, 5000);
}

sayHi()
