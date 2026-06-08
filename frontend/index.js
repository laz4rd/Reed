document.getElementById("upload-form").addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const formData = new FormData();

        formData.append(
            "course",
            document
            .getElementById("course")
            .value
        );

        formData.append(
            "unit",
            document
            .getElementById("unit")
            .value
        );

        formData.append(
            "note_type",
            document
            .getElementById("note_type")
            .value
        );

        const files =
            document
            .getElementById("files")
            .files;

        for (const file of files) {

            formData.append(
                "file",
                file
            );
        }

        const response =
            await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        console.log(data);
    }
);