document.getElementById('verification-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent form from submitting the default way (reloading the page)

    const textInput = document.getElementById('text-input').value;
    const resultDiv = document.getElementById('result');

    if (!textInput) {
        resultDiv.innerHTML = '<span class="failure">Please provide some text.</span>';
        return;
    }

    try {
        const response = await fetch('/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();
        if (data.result) {
            resultDiv.innerHTML = `<span class="success">${data.message}</span>`;
        } else {
            resultDiv.innerHTML = `<span class="failure">${data.message}</span>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<span class="failure">An error occurred: ${error.message}</span>`;
    }
});
