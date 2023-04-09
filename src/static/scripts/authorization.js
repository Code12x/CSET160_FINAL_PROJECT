links_to_add_access_token = document.getElementsByClassName("add_access_token_to_href");
for (i = 0; i < links_to_add_access_token.length; i++) {
    link = links_to_add_access_token[i];
    link.addEventListener('click', (e) => {
        e.preventDefault();

        let url = new URL(link.getAttribute("href"));
        url.searchParams.append("token", localStorage.getItem("access_token"));

        location.assign(url.toString());
    })
}


let logout_form = document.getElementById("logout_form");
logout_form.addEventListener('submit', e => {
    e.preventDefault();

    let req = new XMLHttpRequest();

    req.open("DELETE", "/logout");

    req.setRequestHeader("refresh_token", localStorage.getItem("refresh_token"));

    req.onload = () => {
        res = JSON.parse(req.responseText);
        if (res.logout_status === "success") {
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("access_token");
            location.assign("/");
        } else {
            console.log("Error logging out: " + res);
        }
    };
    req.send();
});


function renew_access_token() {
    req = new XMLHttpRequest();

    req.open("POST", "/token");

    req.setRequestHeader("refresh_token", localStorage.getItem("refresh_token"));

    req.onload = () => {
        res = JSON.parse(req.responseText);
        localStorage.setItem("access_token", res.access_token);
    };
    req.send();
}




