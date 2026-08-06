import dayjs from "dayjs";

console.log("current date:",dayjs().format());
console.log("WiseWheels Global JS Loaded");

frappe.listview_settings["customer_details"] = {
	onload(listview) {
		listview.$page.find(".list-liked-by-me").hide();
	},
	refresh(listview) {
		listview.$page.find(".list-liked-by-me").hide();
		listview.$page.find(".like-action").hide();
	},
};
$(document).on("ajaxComplete", function (event, xhr, settings) {
    if (settings.url && settings.url.includes("frappe.client.delete")) {
        const audio = new Audio("/assets/wisewheels/sounds/delete.mp3");
        audio.play();
    }
});