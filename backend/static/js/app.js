document.addEventListener("DOMContentLoaded", function () {
	const formsetContainer = document.getElementById("formset-container");
	const totalForms = document.getElementById("id_form-TOTAL_FORMS");
	const addFormBtn = document.getElementById("add-form");
	const editUserField = document.getElementById("edit-user-form")
	const userDefinedField = document.getElementById("id_user_defined_field")

	editUserField.addEventListener('click', function () {
		userDefinedField.style.border = "1px solid #ccc";
		userDefinedField.style.pointerEvents = "all";
		userDefinedField.style.cursor = "pointer";
		userDefinedField.focus()
	})
	userDefinedField.addEventListener("blur", function () {
		userDefinedField.style.border = "none";
		userDefinedField.style.pointerEvents = "none";
		userDefinedField.style.cursor = "default";
	});

	addFormBtn.addEventListener("click", function () {
        let formNum = parseInt(totalForms.value);
        lastForm = addFormBtn.previousElementSibling;
        if (checkFormFilled(lastForm)) {
            let newForm = lastForm.cloneNode(true)
            updateFormAttributes(newForm, /form-(\d+)/, `form-${formNum}`);
            newForm.querySelectorAll("input, textarea").forEach((el) => {
                el.value = "";

            });
            newForm.classList.remove("deleted")
            addFormBtn.before(newForm);
            updateFormCount();
        }
	});

	formsetContainer.addEventListener("click", function (event) {
		if (event.target.classList.contains("delete-button")) {
			const currentForm = event.target.parentElement;

			if (!checkFormFilled(currentForm)) {
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
		console.log(forms);
		forms.forEach((el, index) => {
			updateFormAttributes(el, /form-(\d+)/, `form-${index}`);
		});
		totalForms.value = forms.length;
    }
    
    function checkFormFilled(currentForm) {
        return Array.from(currentForm.querySelectorAll('input, textarea')).some(child => {
            return child.value.trim() !== ''
        })
    }
});