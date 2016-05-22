<html>
  <head>
    <title>Authentication Failed - PageObjectLibrary Demo</title>
    <link rel="stylesheet" type="text/css" href="stylesheet.css">
  </head>
  <body>
    <div class="header">
      <a href="/homepage.html">Home</a>&nbsp;
      <a href="/about.html">About</a>&nbsp;
      <span class="align-right"><a href="/admin/shutdown" title="shut down the server">Shut down</a></span>&nbsp;
    </div>
    <div class="content">
    <h1>Authentication failure</h1>

    <b>Unrecognized username/password combination. </b>

    <h2>Please log in</h2>
    <p>
      In the following form, enter any username you want;  the only
      valid password is "<i>password</i>".
    </p>
    <form name="login" action="/authenticate" method="post">
      <div class="entry_field">
        <label for='id_username' class='form_label'>Username:</label>
        <input id='id_username' name='username' class="form_entry">
      </div>
      <div class="entry_field">
        <label for='id_password'class='form_label'>Password:</label>
        <input id='id_password' name='password' class="form_entry">
      </div>
      <p>
      <button type="submit" id='id_submit'>Let's do this!</button>
    </form>
    </div>
  </body>
</html>
