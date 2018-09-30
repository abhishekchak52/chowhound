<form action="/submit" method="post">
    Dal: <select name="Dal">
        % for dal in dals:
        <option value="{{dal}}" 
        % 'selected' if dal in suggested else ''
        > {{dal}}</option>
        % end
        </select>
    Sabzi: <select name="Sabzi">
        % for sabzi in sabzis:
        <option value="{{sabzi}}" 
        % 'selected' if sabzi in suggested else ''
        > {{sabzi}}</option>
        % end
        </select>
    Sweets: <select name="Sweets">
        % for sweet in sweets:
        <option value="{{sweet}}" 
        % 'selected' if sweet in suggested else ''
        > {{sweet}}</option>
        % end
        </select>
    Wastage (% weight): <input name="waste" type="text" />
    <input value="Login" type="submit" />
</form>