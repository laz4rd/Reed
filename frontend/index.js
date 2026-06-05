const formData = new FormData();

formData.append("course", course);
formData.append("unit", unit);
formData.append("note_type", noteType);

for (const file of files) {
    formData.append("files", file);
}