// Mobile nav toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const isOpen = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
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

  // Password show/hide toggle on auth pages
  document.querySelectorAll(".password-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const input = document.getElementById(btn.getAttribute("data-target"));
      if (!input) return;
      const showing = input.type === "text";
      input.type = showing ? "password" : "text";
      btn.textContent = showing ? "show" : "hide";
    });
  });

  function typeText(el, text, speed) {
    let i = 0;
    el.textContent = "";
    const interval = setInterval(() => {
      el.textContent += text.charAt(i);
      i++;
      if (i >= text.length) clearInterval(interval);
    }, speed);
  };



  // auto slide
  const track = document.querySelector(".testimonial-track");

if(track){

    const cards = [...track.children];

    cards.forEach(card => {
        track.appendChild(card.cloneNode(true));
    });

    let index = 0;

    const cardWidth = () => cards[0].offsetWidth + 24;

    function slide(){

        index++;

        track.style.transition = "transform .7s ease";

        track.style.transform =
            `translateX(-${index * cardWidth()}px)`;

        if(index >= cards.length){

            setTimeout(() => {

                track.style.transition = "none";

                track.style.transform = "translateX(0)";

                index = 0;

            },700);

        }

    }

    let autoplay = setInterval(slide,3000);

    track.addEventListener("mouseenter",()=>{

        clearInterval(autoplay);

    });

    track.addEventListener("mouseleave",()=>{

        autoplay = setInterval(slide,3000);

    });

}
});
