const inputs = document.querySelectorAll(".otp-input");
const finalOtp = document.getElementById("final-otp");

inputs.forEach((input, index) => {

input.addEventListener("input", () => {

if(input.value.length === 1 && index < inputs.length - 1){
inputs[index + 1].focus();
}

updateOTP();

});

input.addEventListener("keydown", (e) => {

if(e.key === "Backspace" && input.value === "" && index > 0){
inputs[index - 1].focus();
}

});

});


function updateOTP(){

let otp = "";

inputs.forEach(input => {
otp += input.value;
});

finalOtp.value = otp;

}

