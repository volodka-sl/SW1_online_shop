let register = document.getElementById('registerForm')
let background = document.getElementById('blackbg')
let button = document.getElementById('registerButton')
let name = document.getElementById('name')
let surname = document.getElementById('surname')
let phone = document.getElementById('phone')
let dob = document.getElementById('dob')
let password_conf = document.getElementById('password_conf')
let mail = document.getElementById("mail")
let password = document.getElementById("password")
let right_psw = /^[A-Za-z]\w{7,14}$/
let right_mail = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/
let right_year = /^\d{2}[./-]\d{2}[./-]\d{4}$/
let year = new Date().getFullYear();
const elements_in_doc = [name, surname, phone, mail, dob, password, password_conf]
const data = [name, surname, phone, dob, password_conf]

function clear(arr) {
    for (let i = 0; i < arr.length; i++) {
        arr[i].value = ''
    }
}

function showLoginWindow() {
    let logwindow = document.getElementById('loginwindow')
    if (!logwindow.className.includes('header__loginwindow_after')) {
        logwindow.classList.add('header__loginwindow_after')
    } else {
        logwindow.classList.remove('header__loginwindow_after')
    }
}

function showPassword() {
    let password = document.getElementById('passwordmini')
    let eye = document.getElementById('eyemini')
    if (password.type === 'password') {
        password.type = 'text'
        eye.src = '/static/src/hidedeye.png'
        eye.style.top = '110px'
    } else {
        password.type = 'password'
        eye.src = '/static/src/eye.png'
        eye.style.top = '111px'
    }
}

function openRegForm() {
    clear(elements_in_doc)
    let logwindow = document.getElementById('loginwindow')
    if (!register.className.includes('registerForm_after')) {
        register.classList.add('registerForm_after')
        background.classList.add('blackbg_after')
        logwindow.classList.remove('header__loginwindow_after')
    } else {
        register.classList.remove('registerForm_after')
        background.classList.remove('blackbg_after')
    }
}


function false_fields() {
    for (let i = 0; i < elements_in_doc.length; i++) {
        if (!elements_in_doc[i].value) {
            elements_in_doc[i].style.borderColor = "red"
        } else {
            elements_in_doc[i].style.borderColor = "green"
        }
    }
}

function checkForm() {

    false_fields()
    if (!name.value) {
        alert('Введите имя!')
    } else if (!surname.value) {
        alert('Введите фамилию!')
    } else if (!phone.value) {
        alert('Введите телефон!')
    } else if (!right_mail.test(mail.value)) {
        alert('Неверно введена почта!')
        mail.style.borderColor = "red"
    } else if (!right_psw.test(password.value)) {
        alert('Пароль не соответствует условиям!')
        password.style.borderColor = "red"
        password_conf.style.borderColor = "red"
    } else if (password.value !== password_conf.value) {
        alert('Пароли не совпадают!')
        password_conf.style.borderColor = "red"
    } else if (!right_year.test(dob.value)) {
        alert("Введите дату рождения верного формата: dd.mm.yyyy!")
        dob.style.borderColor = "red"
    } else if (year - dob.value.split(dob.value[2])[2] < 18) {
        alert('Вы слишком малы для регистрации на этом сайте!')
        dob.style.borderColor = "red"
    } else {
        alert("Регистрация успешно завершена!")
        button.type = "submit"
    }
}