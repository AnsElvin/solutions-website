$content = Get-Content -Path "index.html" -Raw -Encoding UTF8
$encoded = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))

$shaResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/AnsElvin/solutions-website/contents/index.html" -Method Get
$sha = $shaResponse.sha

$body = @{
    message = "Fix index.html content"
    content = $encoded
    branch = "main"
    sha = $sha
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/repos/AnsElvin/solutions-website/contents/index.html" -Method Put -Body $body -ContentType "application/json"
Write-Host "Status: Success"
Write-Host "URL: $($response.content.html_url)"