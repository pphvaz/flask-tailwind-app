const cookieName = "userConsent";
const cookiesBanner = document.getElementById("cookies");

function loadGoogleAnalytics() {
    if (localStorage.getItem("cookiesAccepted") === "true") {
        const script = document.createElement("script");
        script.src = "https://www.googletagmanager.com/gtag/js?id=G-FSMV8QZGFQ";
        script.async = true;
        document.head.appendChild(script);

        script.onload = function () {
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            gtag("js", new Date());
            gtag("config", "G-FSMV8QZGFQ");
        };
    }
}

const getConsent= () => {
    const cookieConsent = document.cookie.split("; ").find(row => row.startsWith(`${cookieName}=`))?.split("=")[1];
    const localStorageConsent = localStorage.getItem("cookiesAccepted");
    return cookieConsent || localStorageConsent;
}

if (!getConsent()) {
    cookiesBanner.classList.remove("hidden");
    setTimeout(() => {
        cookiesBanner.classList.remove("opacity-0");
        cookiesBanner.classList.add("opacity-1");
    }, 300);
}

document.getElementById("acceptCookies").addEventListener("click", function () {
    setConsent();
    cookiesBanner.classList.add("opacity-0")
    setTimeout(() => {
        cookiesBanner.classList.add("hidden");
    });
    loadGoogleAnalytics();
});

function setConsent() {
    const expiryDate = new Date();
    expiryDate.setMonth(expiryDate.getMonth() + 6);
    document.cookie = `${cookieName}=true; expires=${expiryDate.toUTCString()}; path=/`;
    localStorage.setItem("cookiesAccepted", "true");
}