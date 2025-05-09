document.addEventListener("DOMContentLoaded", function () {
	// Mobile menu toggle
	const mobileMenuButton = document.getElementById("mobile-menu-button");
	if (mobileMenuButton) {
		mobileMenuButton.addEventListener("click", function () {
			const menu = document.getElementById("mobile-menu");
			menu.classList.toggle("hidden");
			// Toggle aria-expanded for accessibility
			const isExpanded = this.getAttribute("aria-expanded") === "true";
			this.setAttribute("aria-expanded", !isExpanded);
		});
	}
	// Mobile sections toggle
	const mobileSectionsButton = document.getElementById("mobile-sections-button");
	if (mobileSectionsButton) {
		mobileSectionsButton.addEventListener("click", function () {
			console.log("section button clicked")
			const menu = document.getElementById("mobile-sections-menu");
			menu.classList.toggle("w-80");
			button = mobileSectionsButton.firstElementChild
			button.firstElementChild.nextElementSibling.classList.toggle('hidden')
			button.lastElementChild.classList.toggle('hidden')
			// Toggle aria-expanded for accessibility
			const isExpanded = this.getAttribute("aria-expanded") === "true";
			this.setAttribute("aria-expanded", !isExpanded);
		});
	}

	// Auto-dismiss flash messages after 5 seconds
	const flashMessages = document.querySelectorAll(".flash-message");
	if (flashMessages.length > 0) {
		setTimeout(() => {
			flashMessages.forEach((msg) => {
				msg.style.opacity = "0";
				setTimeout(() => msg.remove(), 300);
			});
		}, 5000);

		// Allow manual closing of flash messages
		flashMessages.forEach((msg) => {
			const closeBtn = msg.querySelector(".close-btn");
			if (closeBtn) {
				closeBtn.addEventListener("click", () => {
					msg.style.opacity = "0";
					setTimeout(() => msg.remove(), 300);
				});
			}
		});
	}

	// Enhanced form input validation
	document.querySelectorAll("form").forEach((form) => {
		// Get all form inputs with validation needs
		const inputs = form.querySelectorAll(".form-input[required]");

		inputs.forEach((input) => {
			const errorContainer =
				input.parentNode.querySelector('.text-red-600, [id$="-error"]') ||
				document.createElement("div");

			if (!errorContainer.classList.contains("text-red-600")) {
				errorContainer.className = "mt-1 text-sm text-red-600 h-5";
				input.parentNode.appendChild(errorContainer);
			}

			input.addEventListener("invalid", function (e) {
				e.preventDefault();
				this.classList.add("border-red-500");
				errorContainer.textContent = this.validationMessage;
			});

			input.addEventListener("input", function () {
				if (this.checkValidity()) {
					this.classList.remove("border-red-500");
					errorContainer.textContent = "";
				}
			});

			// Add focus styling
			input.addEventListener("focus", function () {
				this.parentNode
					.querySelector(".text-gray-400")
					?.classList.add("text-purple-500");
			});

			input.addEventListener("blur", function () {
				this.parentNode
					.querySelector(".text-purple-500")
					?.classList.remove("text-purple-500");
			});
			// Disable all submit buttons only when the form is valid
			form.addEventListener("submit", function (e) {
				if (!form.checkValidity()) {
					return;
				}
				const submitButtons = form.querySelectorAll('button[type="submit"]');
				submitButtons.forEach(button => {
					button.disabled = true;
					button.style.pointerEvents = "none";
					button.style.opacity = "0.5";
				});
			});
			
		});

		// Form submission validation
		form.addEventListener("submit", function (e) {
			let formIsValid = true;

			inputs.forEach((input) => {
				if (!input.checkValidity()) {
					input.dispatchEvent(new Event("invalid"));
					formIsValid = false;
				}
			});

			if (!formIsValid) {
				e.preventDefault();
				// Scroll to first invalid input
				const firstInvalid = form.querySelector(".border-red-500");
				if (firstInvalid) {
					firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
				}
			}
		});
	});
	const formsetContainer = document.getElementById("formset-container");
	const totalForms = document.getElementById("id_form-TOTAL_FORMS");
	const addFormBtn = document.getElementById("add-item");
	const editUserField = document.getElementById("edit-user-form");
	const userDefinedField = document.getElementById("id_user_defined_field");

	if (editUserField) {
		editUserField.addEventListener("click", function () {
			userDefinedField.style.border = "1px solid #ccc";
			userDefinedField.style.pointerEvents = "all";
			userDefinedField.style.cursor = "pointer";
			userDefinedField.focus();
		});
	}

	if (userDefinedField) {
		userDefinedField.addEventListener("blur", function () {
			userDefinedField.style.border = "none";
			userDefinedField.style.pointerEvents = "none";
			userDefinedField.style.cursor = "default";
		});
	}

	if (addFormBtn) {
		addFormBtn.addEventListener("click", function () {
			let formNum = parseInt(totalForms.value);
			lastForm = addFormBtn.previousElementSibling;
			if (checkFormFilled(lastForm)) {
				let newForm = lastForm.cloneNode(true);
				updateFormAttributes(newForm, /form-(\d+)/, `form-${formNum}`);
				newForm.querySelectorAll("input, textarea").forEach((el) => {
					el.value = "";
				});
				newForm.classList.remove("deleted");
				addFormBtn.before(newForm);
				updateFormCount();
			} else {
				let warning = addFormBtn.nextElementSibling;
				warning.classList.remove("hidden");
				addFormBtn.disabled = true;
				setTimeout(() => {
					addFormBtn.disabled = false;
					warning.classList.add("hidden");
				}, 2000);
			}
		});
	}

	if (formsetContainer) {
		formsetContainer.addEventListener("click", function (event) {
			if (event.target.classList.contains("delete-button")) {
				const currentForm = event.target.parentElement;

				if (!checkFormFilled(currentForm) && totalForms > 1) {
					currentForm.remove();
				} else {
					currentForm.classList.toggle("deleted");
					if (currentForm.classList.contains("deleted")) {
						updateFormAttributes(currentForm, /form-/, "deleted-form-");
					} else {
						updateFormAttributes(currentForm, /deleted-form-/, "form-");
					}
				}
				updateFormCount();
			}
		});
	}

	function updateFormAttributes(currentForm, from, to) {
		currentForm.querySelectorAll("[name], [for], [id]").forEach((el) => {
			if (el.name) {
				el.name = el.name.replace(from, to);
			}
			if (el.htmlFor) {
				el.htmlFor = el.htmlFor.replace(from, to);
			}
			if (el.id) {
				el.id = el.id.replace(from, to);
			}
		});
	}

	function updateFormCount() {
		formsetForms = formsetContainer.querySelectorAll(".formset-form");
		let forms = Array.from(formsetForms).filter((child) => {
			return !child.classList.contains("deleted");
		});

		forms.forEach((el, index) => {
			updateFormAttributes(el, /form-(\d+)/, `form-${index}`);
		});
		totalForms.value = forms.length;
	}

	function checkFormFilled(currentForm) {
		return Array.from(currentForm.querySelectorAll("input, textarea")).some(
			(child) => {
				return child.value.trim() !== "";
			}
		);
	}
});
