document.addEventListener("DOMContentLoaded", function () {
	const formsetContainer = document.getElementById("formset-container");
	const totalForms = document.getElementById("id_form-TOTAL_FORMS");
	const addFormBtn = document.getElementById("add-form");

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

/* <body>
    
    <form method="post" action="/modify/certificates/6">
        <!-- ----------------------------------- CSRF token ----------------------------------- -->
        <input type="hidden" name="csrfmiddlewaretoken" value="OXXgVS29wYN6qwugj9tSonWhMfmwPdu6PuXGJEjuUliqviZH4n93sS9GXZaES4Iw">
    
    
        <div class="user-defined-field">
            <div>
                <label for="id_user_defined_field">Section:</label>
                <input type="text" name="user_defined_field" value="Certificates" placeholder="Category" id="id_user_defined_field">
            </div>
        </div>
    
    
        <!-- ----------------------------------- Basic Form ----------------------------------- -->
    
    
        <!-- ----------------------------------- Management Form ----------------------------------- -->
        <input type="hidden" name="form-TOTAL_FORMS" value="4" id="id_form-TOTAL_FORMS">
        <input type="hidden" name="form-INITIAL_FORMS" value="4" id="id_form-INITIAL_FORMS">
        <input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS">
        <input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS">
    
    
        <!-- ----------------------------------- Formset Container ----------------------------------- -->
        
        <div id="formset-container">
    
            
            <div class="categories formset-form">
    
                <button type="button" class="delete-button" style="border: none; background-color:crimson; cursor: pointer">DELETE</button>
    
                <div>
                    <input type="text" name="form-0-item" value="Certificate in CS50x Introduction to Computer Science" id="id_form-0-item">
                </div>
            </div>


            <div class="categories formset-form">

                <button type="button" class="delete-button" style="border: none; background-color:crimson; cursor: pointer">DELETE</button>

                <div>
                    <label for="id_form-0-category_name">Section:</label>
                    <input type="text" name="form-0-category_name" value="Extracurricular Activities" id="id_form-0-category_name">
                </div>

                <div>
                    <textarea name="form-0-description" cols="60" rows="10" placeholder="Extra data" id="id_form-0-description">From October 2018 to December 2021, I was an Active Member of Pivot Club, Kenyatta University, where I organized Educational Trips and participated in Talks and Seminars. From May 2014 to November 2015, I was a Member of aviation club, Pioneer School where I was building aeroplane models and  applying Engineering Principles through Networking and Team building Exercises.</textarea>
                </div>

            </div>            
            

            <div class="categories formset-form">
                <button type="button" class="delete-button" style="border: none; background-color:crimson; cursor: pointer">DELETE</button>
                <div>
                    <input type="text" name="form-1-item" value="Certificate in Computer Programming" id="id_form-1-item">
                </div>
            </div>
            
            
            <div class="categories formset-form">
                <button type="button" class="delete-button" style="border: none; background-color:crimson; cursor: pointer">DELETE</button>
                <div>
                    <input type="text" name="form-2-item" value="Kenya Certificate of Secondary Education (KCSE)" id="id_form-2-item">
                </div>
            </div>
            
            
            <div class="categories formset-form">
                <button type="button" class="delete-button" style="border: none; background-color:crimson; cursor: pointer">DELETE</button>
                <div>
                    <input type="text" name="form-3-item" value="Kenya Certificate of Primary Education (KCPE)" id="id_form-3-item">
                </div>
            </div>


            <button type="button" id="add-form" style="border: none; background-color:chartreuse; cursor: pointer; margin: 2rem auto;">ADD</button>

        </div>
        <button type="submit">SUBMIT</button>
    </form>
    
    <div class="nav">
         <a href="/modify/extras/6">Back</a> 
         <a href="/modify/languages/6">Next</a> 
    </div>
    
    <script src="/static/js/app.js"></script>
    

</body> */
