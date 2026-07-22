// Mobile nav toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".nav-links");

// function updateHiddenInput() {

//   const tags = [...document.querySelectorAll(".tag-pill")]
//       .map(tag => tag.childNodes[0].textContent.trim());

//   document.getElementById("tags-hidden").value = tags.join(",");
// }

// updateHiddenInput();

if(toggle && nav){

    toggle.addEventListener("click",()=>{

        const opened = nav.classList.toggle("open");

        toggle.setAttribute("aria-expanded",opened);

        document.body.style.overflow = opened ? "hidden" : "";

    });

    nav.querySelectorAll("a").forEach(link=>{

        link.addEventListener("click",()=>{

            nav.classList.remove("open");

            document.body.style.overflow="";

            toggle.setAttribute("aria-expanded","false");

        });

    });

    window.addEventListener("resize",()=>{

        if(window.innerWidth>900){

            nav.classList.remove("open");

            document.body.style.overflow="";

            toggle.setAttribute("aria-expanded","false");

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

  // Project image dropzone
  const dropzone = document.querySelector("[data-dropzone]");
  if (dropzone) {
    const fileInput = dropzone.querySelector("input[type='file']");
    const filenameEl = dropzone.querySelector(".dropzone-filename");

    dropzone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", () => {
      if (fileInput.files.length) {
        filenameEl.textContent = `Selected: ${fileInput.files[0].name}`;
        filenameEl.style.display = "block";
      }
    });

    ["dragover", "dragleave", "drop"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.toggle("drag-over", evt === "dragover");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        filenameEl.textContent = `Selected: ${e.dataTransfer.files[0].name}`;
        filenameEl.style.display = "block";
      }
    });
  }

  // Tag editor (skills, project tech tags)
  document.querySelectorAll("[data-tag-editor]").forEach((editor) => {

    const list = editor.querySelector(".tag-editor");
    const input = editor.querySelector("[data-tag-input]");
    const hiddenInput = editor.querySelector("#tags-hidden");

    function updateHiddenInput() {

        const tags = [...list.querySelectorAll(".tag-pill")].map(tag => {
            return tag.childNodes[0].textContent.trim();
        });

        hiddenInput.value = tags.join(",");
        console.log(hiddenInput.value);
    }

    function addTag(value){

        const text = value.trim().replace(/,$/, "");

        if(!text) return;

        // Prevent duplicates
        const exists = [...list.querySelectorAll(".tag-pill")].some(tag =>
            tag.childNodes[0].textContent.trim().toLowerCase() === text.toLowerCase()
        );

        if(exists) return;

        const pill = document.createElement("span");

        pill.className = "tag-pill";

        pill.innerHTML = `
            ${text}
            <button type="button" class="tag-remove">&times;</button>
        `;

        pill.querySelector(".tag-remove").addEventListener("click", () => {

            pill.remove();

            updateHiddenInput();

        });

        list.appendChild(pill);

        updateHiddenInput();

    }

    // Existing tags
    list.querySelectorAll(".tag-remove").forEach(btn => {

        btn.addEventListener("click", () => {

            btn.closest(".tag-pill").remove();

            updateHiddenInput();

        });

    });

    input.addEventListener("keydown", function(e){

        if(e.key === "Enter" || e.key === ","){

            e.preventDefault();

            addTag(input.value);

            input.value = "";

        }

    });

    // Initialize hidden input
    updateHiddenInput();

});

  function typeText(el, text, speed) {
    let i = 0;
    el.textContent = "";
    const interval = setInterval(() => {
      el.textContent += text.charAt(i);
      i++;
      if (i >= text.length) clearInterval(interval);
    }, speed);
  }

  document.getElementById("projectForm").addEventListener("submit", function () {

    document.querySelectorAll("[data-tag-editor]").forEach(editor => {

        const list = editor.querySelector(".tag-editor");
        const hidden = editor.querySelector("#tags-hidden");

        hidden.value = [...list.querySelectorAll(".tag-pill")]
            .map(tag => tag.childNodes[0].textContent.trim())
            .join(",");

    });

});
});
