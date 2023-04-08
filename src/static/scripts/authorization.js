links_to_add_access_token = document.getElementsByClassName("add_access_token");
for (i = 0; i < links_to_add_access_token.length - 1; i++) {
    link = links_to_add_access_token[i];
    link.addEventListener('click', (e) => {
        e.preventDefault();

        const headers = { 'Authorization': 'Bearer ' + localStorage.getItem("access_token") };

        fetch(link.getAttribute('href'), { headers })
            .then(response => {
                window.location.href = response.url;
            })
            .catch(error => {
                console.error('Request failed:', error);
            });
    })
}
