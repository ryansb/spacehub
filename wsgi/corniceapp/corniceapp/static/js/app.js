//
// Spacehub
//
App = Ember.Application.create({
	LOG_TRANSITIONS: true,
	authorized: true
});

//
// Utilities
//
App.resetFormValidation = function resetFormValidation(form) {
	$.each($(form).children('.control-group'), function (index, elem) {
		$(elem).removeClass('warning');
		$(elem).removeClass('error');
		$.each($(elem).children('.controls').children('.help-inline'), function (index, help) {
			$(help).html('');
		});
	});
};
App.insertErrorMessage = function insertErrorMessage(element, message) {
	$(element).html($(element).html() + "<p>" + message + "</p>");
};

//
// Router
//
App.Router.map(function () {
	this.route("create", {
		path: "/create"
	});
	this.route("about", {
		path: "/about"
	});
	this.resource("dashboard", {
		path: "/dashboard"
	});
	this.resource("dashboard", {
		path: "/"
	});
	this.resource("signup", {
		path: "/signup"
	});
	this.resource("box", {
		path: "/box/:box_id"
	});
});
//
// Routes
//
App.BoxRoute = Ember.Route.extend({
	model: function (params) {
		return App.Box.find(params.box_id);
	},
	setupController: function (controller, model) {
		controller.set('content', model);
	}
});
App.DashboardRoute = Ember.Route.extend({
	model: function () {
		return App.Box.findAll();
	},
	setupController: function (controller, model) {
		controller.set('content', model);
	}
});
//
// Views
//
App.CreateView = Ember.View.extend({
	didInsertElement: function didInsertElement() {
		// First let's prepend icons (needed for effects)
		$(".checkbox, .radio").prepend("<span class='icon'></span><span class='icon-to-fade'></span>");

		$(".checkbox, .radio").click(function () {
			setupLabel();
		});
		setupLabel();
		$('.has-tip').tooltip();
	}
});
App.BoxView = Ember.View.extend({
	didInsertElement: function didInsertElement() {
		// First let's prepend icons (needed for effects)
		$(".checkbox, .radio").prepend("<span class='icon'></span><span class='icon-to-fade'></span>");

		$(".checkbox, .radio").click(function () {
			setupLabel();
		});
		setupLabel();
		$('.has-tip').tooltip();
	}
});
//
// Controllers
//
App.BoxController = Ember.ObjectController.extend({
	saveBox: function saveBox() {
		var controller = this;
		console.log(controller);
		console.log("Saving box.");
		$.ajax({
			url: "/box/" + controller.content.id,
			type: "PUT",
			data: $("#box-form").serialize(),
			success: function (response) {
				console.log("Successfully saved box.");
				controller.set('content', App.Box.findAll());
				controller.transitionToRoute("dashboard");
			},
			error: function (response) {
				console.log("Failed to save box.");
			}
		});
	},
	deleteBox: function deleteBox() {
		var controller = this;
		console.log("Deleting box.");
		$.ajax({
			url: "/box/" + controller.content.id,
			type: "DELETE",
			success: function (response) {
				console.log("Successfully deleted box.");
				controller.set('content', App.Box.findAll());
				controller.transitionToRoute("dashboard");
			},
			error: function (response) {
				console.log("Failed to delete box.");
			}
		});
	}
});
App.SignupController = Ember.Controller.extend({
	minPasswordLength: 6,
	signUp: function signUp() {
		var controller = this;
		var user = $("#username").val();
		var phone = $("#phone").val();
		var pwd1 = $("#password1").val();
		var pwd2 = $("#password2").val();
		var errors = false;

		App.resetFormValidation('#signup-form');

		if (user.length < 1) {
			errors = true;
			$("#username-control").addClass("warning");
			App.insertErrorMessage("#username-help", "You need a username.");
		}
		if (phone.length < 1) {
			errors = true;
			$("#phone-control").addClass("warning");
			App.insertErrorMessage("#phone-help", "You need a 10-digit U.S. phone number.\n");
		}
		if ((pwd1.length < controller.minPasswordLength) || (pwd2.length < controller.minPasswordLength)) {
			errors = true;
			$("#password-control").addClass("warning");
			App.insertErrorMessage("#password-help", "Your password must be at least 6 characters long.");
		}
		if (pwd1 !== pwd2) {
			errors = true;
			$("#password-control").addClass("warning");
			App.insertErrorMessage("#password-help", "Your password entries don't match. Check your spelling?");
		}

		if (!errors) {
			$.ajax({
				url: "/user",
				type: "POST",
				data: $("#signup-form").serialize(),
				success: function (response) {
					controller.transitionToRoute("dashboard");
					console.log("Successfully created user.");
				},
				error: function (response) {
					console.log("Failed to create user.");
				}
			});
		}
		return false;
	},
	login: function login() {
		var controller = this;
		App.resetFormValidation('#login-form');
		console.log("Passwords match.");
		$.ajax({
			url: "/session",
			type: "POST",
			data: $("#login-form").serialize(),
			success: function (response) {
				controller.transitionToRoute("dashboard");
				console.log("Successfully logged in user.");
				App.set('authorized', true);
			},
			error: function (response) {
				$("#login-control").addClass("error");
				App.insertErrorMessage("#login-password-help", "Unknown username and password combination.");
			}
		});

		return false;
	}
});
App.DashboardController = Ember.ArrayController.extend({});
App.CreateController = Ember.Controller.extend({
	createBox: function createBox() {
		var controller = this;
		$.ajax({
			url: "/box",
			type: "POST",
			data: $("#create-box-form").serialize(),
			success: function (response) {
				controller.set('content', App.Box.findAll());
				controller.transitionToRoute("dashboard");
			},
			error: function (response) {
				console.log("Failed to create new box.");
			}
		});
		return false;
	}
});
App.ApplicationController = Ember.Controller.extend({
	logout: function logout() {
		var app = this;
		$.removeCookie("session");
		app.set('authorized', false);
		location.reload(true);
	}
});
// 
// Models
// 
App.Box = Ember.Object.extend();
App.Box.reopenClass({
	find: function (id) {
		var result = App.Box.create({
			isLoaded: false
		});
		$.getJSON("/box/" + id, function (data) {
			result.setProperties(data);
			result.set('id', data['__id__']);
			result.set('isLoaded', true);
		});
		return result;
	},
	findAll: function () {
		var results = [];
		$.getJSON("/box", function (data) {
			$.each(data, function (index, elem) {
				elem.id = elem.__id__;
				results.pushObject(App.Box.create(elem));
			});
		});
		return results;
	}
});
//
// Initialization
//
$.ajaxSetup({
	statusCode: {
		401: function () {
			window.location.href = "/#/signup";
			App.set('authorized', false);
		}
	}
});