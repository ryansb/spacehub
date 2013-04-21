//
// Spacehub
//
App = Ember.Application.create({
	LOG_TRANSITIONS: true,
	// don't panic, this is only used for showing/hiding
	// a few minor things, like the logout button.
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
	this.route("about", {
		path: "/about"
	});
	this.route("admin", {
		path: "/admin"
	});
	this.route("index", {
		path: "/"
	});
	this.resource("user", {
		path: "/signup"
	});
	this.resource("repo", {
		path: "/repo/:repo_id"
	});
	this.resource("repos", {
		path: "/repos"
	});
	this.resource("newRepo", {
		path: "/new/repo"
	});
});
//
// Routes
//
App.RepoRoute = Ember.Route.extend({
	model: function (params) {
		return App.Repo.find(params.repo_id);
	},
	setupController: function (controller, model) {
		controller.set('content', model);
	}
});
App.ReposRoute = Ember.Route.extend({
	model: function () {
		return App.Repo.findAll();
	},
	setupController: function (controller, model) {
		controller.set('content', model);
	}
});
//
// Views
//
App.RepoView = Ember.View.extend({
	didInsertElement: function didInsertElement() {
		var content = this.controller.content;
		$("input[value=" + content.source_type + "]").attr('checked', 'checked');
	}
});
//
// Controllers
//
//  
App.NewRepoController = Ember.Controller.extend({
	postRepo: function postRepo() {
		var controller = this;
		console.log("Creating repo.");

		var name = $("#repo-name").val();
		var github_uname = $("#repo-github-user").val();
		var github_repo = $("#repo-github-name").val();
		var source_url = $("#repo-source-url").val();
		var source_type = $('input[name=repo-source-type]:checked').val();
		body = {
			"name": name,
			"github_uname": github_uname,
			"github_repo": github_repo,
			"source_url": source_url,
			"source_type": source_type
		};
		$.ajax({
			url: "/repo",
			type: "POST",
			data: JSON.stringify(body),
			success: function (response) {
				console.log("Successfully created repo.");
			},
			error: function (response) {
				console.log("Failed to create repo.");
			}
		});
	}
});
App.RepoController = Ember.ObjectController.extend({
	putRepo: function putRepo() {
		var controller = this;
		console.log(controller);
		console.log("Saving Repo.");
		var name = $("#repo-name").val();
		var github_uname = $("#repo-github-user").val();
		var github_repo = $("#repo-github-name").val();
		var source_url = $("#repo-source-url").val();
		var source_type = $('input[name=repo-source-type]:checked').val();
		body = {
			"name": name,
			"github_uname": github_uname,
			"github_repo": github_repo,
			"source_url": source_url,
			"source_type": source_type
		};
		$.ajax({
			url: "/repo/" + controller.content.id,
			type: "PUT",
			data: JSON.stringify(body),	
			success: function (response) {
				console.log("Successfully saved repo.");
				controller.set('content', App.Repo.findAll());
				controller.transitionToRoute("repos");
			},
			error: function (response) {
				console.log("Failed to save repo.");
			}
		});
	},
	deleteRepo: function deleteRepo() {
		var controller = this;
		console.log("Deleting repo.");
		$.ajax({
			url: "/repo/" + controller.content.id,
			type: "DELETE",
			success: function (response) {
				console.log("Successfully deleted repo.");
				controller.set('content', App.Repo.findAll());
				controller.transitionToRoute("repos");
			},
			error: function (response) {
				console.log("Failed to delete repo.");
			}
		});
	}
});
App.UserController = Ember.Controller.extend({
	minPasswordLength: 6,
	postUser: function postUser() {
		var controller = this;
		var user = $("#username").val();
		var email = $("#email").val();
		var pwd1 = $("#password1").val();
		var pwd2 = $("#password2").val();
		var errors = false;

		App.resetFormValidation('#signup-form');

		if (user.length < 1) {
			errors = true;
			$("#username-control").addClass("warning");
			App.insertErrorMessage("#username-help", "You need a username.");
		}
		if (email.length < 1) {
			errors = true;
			$("#email-control").addClass("warning");
			App.insertErrorMessage("#email-help", "You need an email address.\n");
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

		var body = {
			"username": user,
			"email": email, 
			"password": pwd1
		}

		if (!errors) {
			$.ajax({
				url: "/users",
				type: "POST",
				data: JSON.stringify(body),
				success: function (response) {
					controller.transitionToRoute("repos");
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
		body = {
			username:  $("#login-username").val(),
			password: $("#login-password").val()
		}
		$.ajax({
			url: "/users/login",
			type: "POST",
			data: JSON.stringify(body),
			success: function (response) {
				controller.transitionToRoute("repos");
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
App.ReposController = Ember.ArrayController.extend({});
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
App.Repo = Ember.Object.extend();
App.Repo.reopenClass({
	find: function (id) {
		var result = App.Repo.create({
			isLoaded: false
		});
		$.getJSON("/repo/" + id, function (data) {
			result.setProperties(data);
			// result.set('id', data['__id__']);
			result.set('isLoaded', true);
		});
		return result;
	},
	findAll: function () {
		var results = [];
		$.getJSON("/repo", function (data) {
			$.each(data["repos"], function (index, elem) {
				// elem.id = elem.__id__;
				results.pushObject(App.Repo.create(elem));
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