<h1>ChowHound</h1>

<form action="/submit" method="post">
% print(suggested)
    Dal: <select name="Dal">
        % for dal in dals:
        <option value="{{dal}}" 
        % if dal == suggested[0]:
            selected
        %end
        > {{dal}}</option>
        % end
        </select>
    Sabzi: <select name="Sabzi">
        % for sabzi in sabzis:
        <option value="{{sabzi}}" 
        % if sabzi == suggested[1]:
            selected
        %end
        > {{sabzi}}</option>
        % end
        </select>
    Sweets: <select name="Sweets">
        % for sweet in sweets:
        <option value="{{sweet}}" 
        % if sweet == suggested[2]:
            selected
        %end
        > {{sweet}}</option>
        % end
        </select>
    Wastage (% weight): <input name="waste" type="text" />
    <input value="Login" type="submit" />
</form>