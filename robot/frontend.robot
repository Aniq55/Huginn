*** Settings ***
Suite Setup    Start Huginn
Suite Teardown    Stop Huginn
Library    RequestsLibrary
Library    Collections
Resource    Huginn.robot

*** Test Cases ***
Front-end is ready
    [Documentation]    This test checks if the front end is displayed when you connect to the web server
    [Tags]    frontend
    Create Session    huginn_web_server    ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /
    Should be Equal As Strings    ${resp.status_code}  200
    Should Contain    ${resp.text}  Flight simulator data viewer
