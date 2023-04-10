function test_path_for_auth(url_href) {
    let req = new XMLHttpRequest();

    let url = new URL(url_href);


    req.open("GET", url.href);

    req.onload = () => {
        try {
            response = JSON.parse(req.responseText);

            if (response.status === "invalid") {
                renew_access_token();
                test_path_for_auth(url.href);
            } else if (response.status === "error") {
                if (response.error === "missing access token") {
                    if (localStorage.getItem("access_token")) {
                        url.searchParams.set("token", localStorage.getItem("access_token"));
                        test_path_for_auth(url.href);
                    } else {
                        location.assign("/login?next=" + url.href)
                    }
                }
            } else {
                window.location.assign(url.href);
            }
        } catch {
            window.location.assign(url.href);
        }
    }
    req.send();
}

links_to_add_access_token = document.getElementsByTagName("a");
for (i = 0; i < links_to_add_access_token.length; i++) {
    let link = links_to_add_access_token[i];

    href = link.href;

    let url = new URL(href);

    if (url.host === location.host) {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            test_path_for_auth(url.href);
        })
    }
}


function renew_access_token(url = undefined) {
    req = new XMLHttpRequest();

    req.open("POST", "/token");

    req.onload = () => {
        res = JSON.parse(req.responseText);
        if (res.status === "success") {
            localStorage.setItem("access_token", res.access_token);
        } else {
            if (url) {
                test_path_for_auth("/login?next=" + url);
            } else {
                location.assign("/login");
            }
        }
    };
    req.send();
}
