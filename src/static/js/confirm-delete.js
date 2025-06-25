function confirmDelete(productId, productName) {
    if (confirm(`Tem certeza que deseja deletar o produto "${productName}" (ID: ${productId})? Esta ação é irreversível!`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `{{ url_for('produtos.deletar_produto', produto_id='0') }}`.replace('0', productId);

        document.body.appendChild(form);
        form.submit();
    }
}