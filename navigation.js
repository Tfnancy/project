const navigation = document.querySelector(".masthead nav");
const compactLayout = window.matchMedia("(max-width: 880px)");
const menuButton = document.createElement("button");
menuButton.type = "button";
menuButton.className = "menu-button";
menuButton.textContent = "Menu";
menuButton.setAttribute("aria-controls", "main-navigation");
navigation.id = "main-navigation";
navigation.before(menuButton);

function setMenu(open) {
  navigation.hidden = !open;
  menuButton.setAttribute("aria-expanded", String(open));
}

function adaptMenu() {
  const focusWasInMenu = navigation.contains(document.activeElement);
  menuButton.hidden = !compactLayout.matches;
  setMenu(!compactLayout.matches);
  if (compactLayout.matches && focusWasInMenu) menuButton.focus();
}

menuButton.addEventListener("click", () => setMenu(navigation.hidden));
document.querySelector(".masthead").addEventListener("keydown", (event) => {
  if (event.key === "Escape" && compactLayout.matches && !navigation.hidden) {
    setMenu(false);
    menuButton.focus();
  }
});
compactLayout.addEventListener("change", adaptMenu);
adaptMenu();
