/* Kirish / ro'yxat sahifasi: rolga qarab tug'ilgan sana maydonini ko'rsatish */
(function () {
  "use strict";
  const roleInputs = document.querySelectorAll('input[name="role"]');
  const birthField = document.getElementById("birthField");
  if (!roleInputs.length || !birthField) return;

  function sync() {
    const checked = document.querySelector('input[name="role"]:checked');
    const isChild = checked && checked.value === "bola";
    birthField.style.display = isChild ? "" : "none";
  }
  roleInputs.forEach((r) => r.addEventListener("change", sync));
  sync();
})();
