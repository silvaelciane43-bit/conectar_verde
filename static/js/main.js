document.addEventListener('DOMContentLoaded', () => {
    const fotoInput = document.getElementById('foto');
    const previewContainer = document.getElementById('image-preview');
    const form = document.querySelector('form');

    // Pré-visualização da imagem
    if (fotoInput) {
        fotoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 200px; margin-top: 10px; border-radius: 8px;">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Validação básica do formulário
    if (form) {
        form.addEventListener('submit', function(e) {
            const descricao = document.getElementById('descricao');
            if (!fotoInput.value || (descricao && !descricao.value.trim())) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos e selecione uma imagem.');
            }
        });
    }
});
