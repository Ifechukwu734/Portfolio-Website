// Mobile nav toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");

if (toggle && links) {

    toggle.addEventListener("click", () => {

        const open = links.classList.toggle("open");

        toggle.setAttribute("aria-expanded", open);

        document.body.style.overflow = open ? "hidden" : "";
    });

    // Close menu when a link is clicked
    links.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            links.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
            document.body.style.overflow = "";
        });
    });

    // Close menu when screen becomes desktop
    window.addEventListener("resize", () => {
        if (window.innerWidth > 900) {
            links.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
            document.body.style.overflow = "";
        }
    });
}

  // Live clock in status bar
  const clock = document.querySelector("[data-clock]");
  if (clock) {
    const update = () => {
      const now = new Date();
      const h = String(now.getHours()).padStart(2, "0");
      const m = String(now.getMinutes()).padStart(2, "0");
      clock.textContent = `${h}:${m} local`;
    };
    update();
    setInterval(update, 15000);
  }

  // Terminal typing effect on hero
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const typeTargets = document.querySelectorAll("[data-type]");

  if (typeTargets.length) {
    if (reduceMotion) {
      typeTargets.forEach((el) => {
        el.textContent = el.getAttribute("data-type");
      });
    } else {
      let delay = 0;
      typeTargets.forEach((el) => {
        const text = el.getAttribute("data-type");
        const speed = 22;
        setTimeout(() => typeText(el, text, speed), delay);
        delay += text.length * speed + 350;
      });
    }
  }

  function typeText(el, text, speed) {
    let i = 0;
    el.textContent = "";
    const interval = setInterval(() => {
      el.textContent += text.charAt(i);
      i++;
      if (i >= text.length) clearInterval(interval);
    }, speed);
  }
});
