function sayHi() {
    console.log('Hi,', process.env.NAME, 'at', Date.now());
    setTimeout(sayHi, 5000);
}

sayHi()
