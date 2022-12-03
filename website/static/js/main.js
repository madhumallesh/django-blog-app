$(document).ready(function () {
	$("#userNotification").hide();
	$(".fakepasswordicon").on("click", function () {
		if ($(".fakepassword").attr("type") === "password") {
			$(".fakepasswordicon").removeClass("fa-eye-slash").addClass("fa-eye");
			$(".fakepassword").attr("type", "text");
		} else if ($(".fakepassword").attr("type") == "text") {
			$(".fakepasswordicon").removeClass("fa-eye").addClass("fa-eye-slash");
			$(".fakepassword").attr("type", "password");
		}
	});
});
