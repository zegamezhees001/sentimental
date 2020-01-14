/**
 *
 * @param {*} eleName
 * @param {*} className
 * @param {*} textInput
 * @param {*} funcOnclick is function when click
 */
function createElementFun(eleName, className, textInput, funcOnclick) {
  const createElement = document.createElement(eleName);
  if (textInput) {
    const ctn = document.createTextNode(textInput);
    createElement.appendChild(ctn);
  }
  if (className) createElement.className = className;
  if (funcOnclick) createElement.onclick = funcOnclick;
  return createElement;
}

/**
 *
 * @param {*} element element is cleared.
 */
function removeChild(element) {
  while (element.firstChild) {
    element.firstChild.remove();
  }
}

/**
 *
 * @param {*} message
 * @param {*} classShow class 2 class err-message with success choose 1 to detect message err or success in style css.
 */
function message_show_success(message, classShow) {
  const messageEle = document.getElementById("message-create-user");
  messageEle.style.display = "block";
  messageEle.innerHTML = message;
  messageEle.className = classShow;
  const createX = createElementFun("i", "far fa-window-close");
  messageEle.appendChild(createX);
}
