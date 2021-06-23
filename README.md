# FamilyBudget

An app for managing the family budget


<h2>Instructions for running locally</h2>
<ol style="bullet-style: none;">
  <li>Git clone</li>
  <li>Run "pip install -r requirements.txt" (preferably in a virtual env)</li>
  <li>Run a file called "run_locally.bat"</li>
  <li>Log in as "FamilySpirit" with the password "123"</li>
  <li>Optionall log in as other family members to see some budgets, their passwords are always "123"</li>
</ol>
<p>Since I was not using a framework like React I decided to render JS partially with Django Templates and then pull data from REST frameworks with simple JS fetches
to imitate the behaviour of a Django + React configuration, where Django serves mostly for serving JSON data and validating JWTs etc.</p>
<br>
<h3>Things that are there</h3>

<ul>
  <li>A dashboard written in Django and vanilla JS + boostrap & jQuery</li>
  <li>Creating + sharing budgets</li>
  <li>Investigating budget details</li>
  <li>Creating users</li>
  <li>Editing users (one can only edit his own account)</li>
</ul>
<br>
<h3>Things that are not there or could be improved</h3>
<p>Due to time constraints I was not able to implement all features, that I intended to.</p>
<ul>
  <li>Updating / editing budgets is not possible yet</li>
  <li>Testing is very limited (only main functionalities)</li>
  <li>Pagination and filtering is done on the client's side, which should not be a problem for a simple app like this, with a limited number of results, however it chould be moved to the backend for a performance boost if needed</li>
</ul>
