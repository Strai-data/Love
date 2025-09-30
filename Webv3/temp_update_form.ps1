$path = 'c:\Users\lansh\OneDrive\Documents\Webbb\index.html'
$text = Get-Content -Raw $path
$pattern = '<form id="ring-size-form" class="ring-size-form" name="ring-size" method="POST" data-netlify="true" data-netlify-honeypot="petal" autocomplete="off" novalidate>`n        <input type="hidden" name="form-name" value="ring-size">`n        <div hidden aria-hidden="true">`n            <label for="petal-field">Leave this field empty if you''re human.</label>`n            <input id="petal-field" name="petal" type="text" tabindex="-1" autocomplete="off">`n        </div>'
$replacement = @"
<form id="ring-size-form" class="ring-size-form" name="ring-size" method="POST" data-netlify="true" data-netlify-honeypot="petal" autocomplete="off" novalidate>
        <input type="hidden" name="form-name" value="ring-size">
        <div hidden aria-hidden="true">
            <label for="petal-field">Leave this field empty if you're human.</label>
            <input id="petal-field" name="petal" type="text" tabindex="-1" autocomplete="off">
        </div>
"@
if ($text -notlike "*$pattern*") {
    throw 'Pattern not found'
}
$text = $text.Replace($pattern, $replacement)
Set-Content -Path $path -Value $text
