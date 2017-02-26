function getStream() {
	$.ajax({
		url: "/socialnetwork3/getstream",
		data: "csrfmiddlewaretoken="+getCSRFToken(),
		dataType: "json",
		success: updateStream
	});
}

function updateStream(posts) {
	$("ol li").remove();
	$(posts).each(function() {
		$("#posts").append(
			'<li><form method="post" action="/socialnetwork3/profile"><div class="row" style="background: white; margin-bottom: 10px; width: 100%;"><img src="/socialnetwork3/photo/'+
			this.user_id+
			'" width="100px" height="100px" style="margin: 10px;"><div class="column" style="width: 100%"><div class="row" id="personal"><p>'+
			this.first_name+
			'</p><p>&nbsp</p><p>'+
			this.last_name+
			'</p><p>&nbsp &nbsp</p><button type="submit" name="username" id="username" value="'+
			this.username+
			'">'+
			this.username+
			'</button><p>&nbsp &nbsp</p><p style="color: grey; font-weight: 300;">'+
			this.date+
			'</p><p>&nbsp &nbsp &nbsp</p><button type="submit" name="follow" id="username" value="Follow">Follow</button><p>&nbsp &nbsp &nbsp</p><button type="submit" name="unfollow" id="username" value="Unfollow">Unfollow</button><input type="hidden" name="followuser" value="'+
			this.username+
			'"></div><div class="row" id="content"><p>'+
			this.post+
			'</p></div></div></div><input type="hidden" name="csrfmiddlewaretoken" value="'+
			getCSRFToken()+
			'"></form></li>');
	});
}

function generateURL(keyword) {
	return "{% url some_url %}".replace("some_url", keyword)
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

$(document).ready(function() {
	getStream();
	setInterval(getStream, 5000);
});