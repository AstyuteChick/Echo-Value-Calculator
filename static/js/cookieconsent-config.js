CookieConsent.run({
    guiOptions: {
        consentModal: {
            layout: "box",
            position: "bottom right",
            equalWeightButtons: true,
            flipButtons: false
        },
        preferencesModal: {
            layout: "box",
            equalWeightButtons: true,
            flipButtons: false
        }
    },

    categories: {
        necessary: {
            enabled: true,
            readOnly: true
        },

        analytics: {
            enabled: false,
            readOnly: false,

            autoClear: {
                cookies: [
                    { name: /^_ga/ },
                    { name: "_gid" }
                ]
            },

            services: {
                ga: {
                    label: "Google Analytics",
                    cookies: [
                        { name: /^_ga/ },
                        { name: "_gid" }
                    ]
                }
            }
        }
    },

    onConsent: function () {
        updateGoogleConsent();
    },

    onChange: function () {
        updateGoogleConsent();
    },

    language: {
        default: "en",

        translations: {
            en: {
                consentModal: {
                    title: "Cookies?",
                    description:
                        "Necessary cookies keep the site working, while optional analytics help me improve the calculator much faster, by letting me spot issues and understand what users use",
                    acceptAllBtn: "Accept optional",
                    acceptNecessaryBtn: "Reject optional",
                    showPreferencesBtn: "Manage choices"
                },

                preferencesModal: {
                    title: "Cookie preferences",
                    acceptAllBtn: "Accept all",
                    acceptNecessaryBtn: "Reject optional",
                    savePreferencesBtn: "Save choices",
                    closeIconLabel: "Close",

                    sections: [
                        {
                            title: "Cookie usage",
                            description:
                                "You can choose which optional cookies are allowed. Necessary cookies are always enabled because they are required for basic website functionality."
                        },

                        {
                            title: "Necessary cookies",
                            description:
                                "Required for core functionality, such as remembering your cookie choice and site preferences.",
                            linkedCategory: "necessary"
                        },

                        {
                            title: "Analytics cookies",
                            description:
                                "Help improve Echo Value Calculator with anonymous usage stats — like which calculators are used most and where things might need fixing. No ads, no selling data, just better tools.",
                            linkedCategory: "analytics"
                        },

                        {
                            title: "More information",
                            description:
                                'For details, see the <a href="/privacy">Privacy Policy</a>.'
                        }
                    ]
                }
            }
        }
    }
});


function updateGoogleConsent() {
    if (typeof gtag !== "function") {
        return;
    }

    const analyticsAccepted = CookieConsent.acceptedCategory("analytics");

    gtag("consent", "update", {
        analytics_storage: analyticsAccepted ? "granted" : "denied",

        ad_storage: "denied",
        ad_user_data: "denied",
        ad_personalization: "denied",

        functionality_storage: "granted",
        security_storage: "granted"
    });
}


const cookieSettingsBtn = document.querySelector("#cookie-settings-btn");

if (cookieSettingsBtn) {
    cookieSettingsBtn.addEventListener("click", function () {
        CookieConsent.showPreferences();
    });
}
