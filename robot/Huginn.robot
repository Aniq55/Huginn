*** Settings ***
Library    Process
Library    String
Library    RequestsLibrary
Library    Collections

*** Variables ***
${HUGINN_URL}    http://localhost:8090
${IC_X_ACCELERATION}    -2.3863054128
${IC_Y_ACCELERATION}    0.300261528
${IC_Z_ACCELERATION}    -8.0968135752
${IC_P}    1.2017789753
${IC_Q}    -3.218303935
${IC_R}    1.1054074741
${IC_PRESSURE}    97771.68
${IC_TOTAL_PRESSURE}    98224.25
${IC_AIRSPEED}    27.5779647576
${IC_CLIMB_RATE}    -0.5705791992
${IC_U_DOT}    -1.9936925328
${IC_V_DOT}    -0.0348145608
${IC_W_DOT}    0.109516164
${IC_P_DOT}    0.45928296858
${IC_Q_DOT}    -1.2179936809
${IC_R_DOT}    -0.20334272149
${IC_GRAVITY}    9.7952561016
${IC_U}    27.568844532
${IC_V}    -0.1193944272
${IC_W}    -0.712468476
${IC_CALIBRATED_AIRSPEED}    27.1740273384
${IC_EQUIVALENT_AIRSPEED}    27.1825690536
${IC_GROUND_SPEED}    27.572404596
${IC_PHI}    1.083614
${IC_THETA}    -2.670314
${IC_PSI}    46.019295

*** Keywords ***
Start Huginn
    ${huginn_process_id} =    Start Process    huginn_start    shell=true
    Process Should Be Running    ${huginn_process_id}
    Create Session    huginn_web_server    ${HUGINN_URL}
    Wait Until Keyword Succeeds    1 min    1 sec    Get Request    huginn_web_server    /
    Simulator Is Paused
    Simulator DT Should Be    0.003333
    Simulation Time Should Be Close To    1.0  0.1
    
Stop Huginn
    Terminate All Processes

Resume Simulation Using The CLI
    ${result} =    Run Process    huginn_control resume  shell=true
    Should Be Equal As Integers    ${result.rc}  0

Pause the Simulation Using The CLI
    ${result} =    Run Process    huginn_control pause  shell=true
    Should Be Equal As Integers    ${result.rc}  0

Reset the Simulation Using The CLI
    ${result} =    Run Process    huginn_control reset  shell=true
    Should Be Equal As Integers    ${result.rc}  0

Value Close To
    [Arguments]    ${value}    ${expected_value}    ${tolerance}
    Should Be True    ${value} >= ${expected_value} - ${tolerance} 
    Should Be True    ${value} <= ${expected_value} + ${tolerance}    

Simulator Command Executed Successfully
    [Arguments]    ${response}    ${command}
    Response Status Code Should Be    ${response}  200
    Dictionary Should Contain Key    ${response.json()}    command
    Dictionary Should Contain Key    ${response.json()}    result
    Should be Equal As Strings    ${response.json()['command']}    ${command}
    Should be Equal As Strings    ${response.json()['result']}    ok

Execute Simulator Control Command
    [Arguments]    ${session}    ${command}
    ${command_data} =    Create Dictionary  command=${command}
    ${headers}=  Create Dictionary  Content-Type=application/json
    ${resp} =    Post Request    huginn_web_server  /simulator  data=${command_data}  headers=${headers}
    [Return]    ${resp}

JSON Response Should Contain item
    [Arguments]    ${response}  ${item}
    Dictionary Should Contain Key    ${response.json()}  ${item}

Response Content Type Should Be JSON
    [Arguments]    ${response}
    ${content_type} =    Get Substring    ${response.headers['content-type']}  0  16
    Should Be Equal    ${content_type}    application/json

Simulator Is Running
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  running
    ${running} =    Convert To Boolean    ${resp.json()['running']}
    Should Be True    ${running}

Simulator Is Paused
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  running
    ${running} =    Convert To Boolean    ${resp.json()['running']}
    Should Not Be True    ${running}

Simulator DT Should Be
    [Arguments]    ${dt}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  dt
    Should Be Equal As Numbers    ${resp.json()['dt']}  ${dt}

Simulation Time Should Be Close To
    [Arguments]    ${time}  ${difference}=0.1
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  time
    ${min_value} =    Set Variable    ${time} - ${difference}
    Should Be True    ${resp.json()['time']} >= ${min_value}
    ${max_value} =    Set Variable    ${time} + ${difference}
    Should Be True    ${resp.json()['time']} <= ${max_value}

Simulation Time Should Be Greater Than
    [Arguments]    ${time}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  time
    Should Be True    ${resp.json()['time']} > ${time}

Response Status Code Should Be
    [Arguments]    ${response}  ${status_code}
    Should be Equal As Integers    ${response.status_code}  ${status_code}

Send Get HTTP Command
    [Arguments]    ${command_url}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  ${command_url}
    [Return]    ${resp}

Resume Simulation
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  resume
    Simulator Command Executed Successfully    ${resp}  resume

Reset Simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  reset
    Simulator Command Executed Successfully    ${resp}  reset

Pause Simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  pause
    Simulator Command Executed Successfully    ${resp}  pause

Get Simulator Time
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  time
    ${simulator_time} =    Convert To Number    ${resp.json()['time']}
    [Return]    ${simulator_time}

Execute Single Simulation Step
    ${resp} =    Execute Simulator Control Command    huginn_web_server  step
    Simulator Command Executed Successfully    ${resp}  step

Run The Simulation For The Given Time
    [Arguments]    ${time_to_run}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${command_data} =    Create Dictionary  command=run_for  time_to_run=${time_to_run}
    ${headers}=  Create Dictionary  Content-Type=application/json
    ${resp} =    Post Request    huginn_web_server  /simulator  data=${command_data}  headers=${headers}
    Simulator Command Executed Successfully    ${resp}  run_for

Aircraft Should Be In The Start Location
    ${resp} =    Get Request    huginn_web_server  /aircraft/instruments/gps
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  latitude
    JSON Response Should Contain item    ${resp}  longitude
    JSON Response Should Contain item    ${resp}  altitude
    JSON Response Should Contain item    ${resp}  airspeed
    JSON Response Should Contain item    ${resp}  heading
    Value Close To    ${resp.json()['latitude']}  37.923255  0.001
    Value Close To    ${resp.json()['longitude']}  23.921773  0.001
    Value Close To    ${resp.json()['altitude']}  300.00000  10.0
    Value Close To    ${resp.json()['airspeed']}  30.00000  5.0
    Value Close To    ${resp.json()['heading']}  45.00000  5.0

Get FDM Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm
    [Return]    ${resp}

Is Valid FDM Data Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  time
    JSON Response Should Contain item    ${response}  dt
    JSON Response Should Contain item    ${response}  latitude
    JSON Response Should Contain item    ${response}  longitude
    JSON Response Should Contain item    ${response}  altitude
    JSON Response Should Contain item    ${response}  airspeed
    JSON Response Should Contain item    ${response}  heading
    JSON Response Should Contain item    ${response}  aileron
    JSON Response Should Contain item    ${response}  elevator
    JSON Response Should Contain item    ${response}  rudder
    JSON Response Should Contain item    ${response}  throttle
    JSON Response Should Contain item    ${response}  x_acceleration
    JSON Response Should Contain item    ${response}  y_acceleration
    JSON Response Should Contain item    ${response}  z_acceleration
    JSON Response Should Contain item    ${response}  roll_rate
    JSON Response Should Contain item    ${response}  pitch_rate
    JSON Response Should Contain item    ${response}  yaw_rate
    JSON Response Should Contain item    ${response}  temperature
    JSON Response Should Contain item    ${response}  static_pressure
    JSON Response Should Contain item    ${response}  total_pressure
    JSON Response Should Contain item    ${response}  roll
    JSON Response Should Contain item    ${response}  pitch
    JSON Response Should Contain item    ${response}  thrust

Is FDM Data Response With Aircraft In The Start Location
    [Arguments]    ${response}
    Value Close To    ${response.json()['latitude']}  37.923255  0.001
    Value Close To    ${response.json()['longitude']}  23.921773  0.001
    Value Close To    ${response.json()['altitude']}  300.00000  10.0
    Value Close To    ${response.json()['airspeed']}  30.00000  5.0
    Value Close To    ${response.json()['heading']}  45.00000  5.0
    Should Be Equal As Numbers    ${response.json()['aileron']}  0.00000  precision=4
    Should Be Equal As Numbers    ${response.json()['elevator']}  0.00000  precision=4
    Should Be Equal As Numbers    ${response.json()['rudder']}  0.00000  precision=4
    Should Be Equal As Numbers    ${response.json()['throttle']}  0.00000  precision=4
    Value Close To    ${response.json()['roll']}  0.00000  5.0
    Value Close To    ${response.json()['pitch']}  0.00000  5.0
    Should Be Equal As Numbers    ${response.json()['x_acceleration']}  ${IC_X_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['y_acceleration']}  ${IC_Y_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['z_acceleration']}  ${IC_Z_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['roll_rate']}  ${IC_P}  precision=4
    Should Be Equal As Numbers    ${response.json()['pitch_rate']}  ${IC_Q}  precision=4
    Should Be Equal As Numbers    ${response.json()['yaw_rate']}  ${IC_R}  precision=4
    Value Close To    ${response.json()['total_pressure']}  ${IC_TOTAL_PRESSURE}  1.0
    Value Close To    ${response.json()['static_pressure']}  ${IC_PRESSURE}  1.0

Get GPS Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${response} =    Get Request    huginn_web_server  /aircraft/instruments/gps
    [Return]    ${response}

Should Be Valid GPS Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  latitude
    JSON Response Should Contain item    ${response}  longitude
    JSON Response Should Contain item    ${response}  altitude
    JSON Response Should Contain item    ${response}  airspeed
    JSON Response Should Contain item    ${response}  heading

Should Be GPS Response When Aircraft Is In The Start Location
    [Arguments]    ${response}
    Value Close To    ${response.json()['latitude']}  37.923255  0.005
    Value Close To    ${response.json()['longitude']}  23.921773  0.005
    Value Close To    ${response.json()['altitude']}  300.00000  30.0
    Value Close To    ${response.json()['airspeed']}  30.00000  5.0
    Value Close To    ${response.json()['heading']}  45.00000  5.0

Get Accelerometer Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${response} =    Get Request    huginn_web_server  /aircraft/sensors/accelerometer
    [Return]    ${response}

Should Be Valid Accelerometer Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  x
    JSON Response Should Contain item    ${response}  y
    JSON Response Should Contain item    ${response}  z

Should Be Accelerometer Response With Aircraft Almost Level
    [Arguments]    ${response}
    Value Close To    ${response.json()['x']}  0.0  5.0
    Value Close To    ${response.json()['y']}  0.0  5.0
    Value Close To    ${response.json()['z']}  -9.8  5.0

Get Gyroscope Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/sensors/gyroscope
    [Return]    ${resp}

Should Be Valid Gyroscope Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  roll_rate
    JSON Response Should Contain item    ${response}  pitch_rate
    JSON Response Should Contain item    ${response}  yaw_rate

Should Be Gyroscope Response With Minimal Aircraft Rotation
    [Arguments]    ${response}
    Value Close To    ${response.json()['roll_rate']}  0.0  5.0
    Value Close To    ${response.json()['pitch_rate']}  0.0  5.0
    Value Close To    ${response.json()['yaw_rate']}  0.0  5.0

Get Thermometer Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/sensors/thermometer
    [Return]    ${resp}

Should Be Valid Thermometer Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  temperature

Should Be Valid Thermometer Response When Aircraft At 300 Meters Above Sea Level
    [Arguments]    ${response}
    Value Close To    ${response.json()['temperature']}  280.0  10.0

Get Pressure Sensor Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/sensors/pressure_sensor
    [Return]    ${resp}

Should Be Valid Pressure Sensor Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  static_pressure

Should Be Pressure Sensor Response When Aircraft At 300 Meters Above Sea Level
    [Arguments]    ${response}
    Value Close To    ${response.json()['static_pressure']}  97000.0  5000.0

Get Pitot Tube Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/sensors/pitot_tube
    [Return]    ${resp}

Should Be Valid Pitot Tube Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  total_pressure

Should Be Pitot Tube Response When Airspeed At 30 Meters Per Second
    [Arguments]    ${response}
    Value Close To    ${response.json()['total_pressure']}  97000.0  5000.0

Get INS Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/sensors/ins
    [Return]    ${resp}

Should Be Valid INS Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  latitude
    JSON Response Should Contain item    ${response}  longitude
    JSON Response Should Contain item    ${response}  altitude
    JSON Response Should Contain item    ${response}  airspeed
    JSON Response Should Contain item    ${response}  heading
    JSON Response Should Contain item    ${response}  pitch
    JSON Response Should Contain item    ${response}  roll

Should Be Valid INS Response When Aircraft In The Start Location
    [Arguments]    ${response}
    Value Close To    ${response.json()['latitude']}  37.923255  0.005
    Value Close To    ${response.json()['longitude']}  23.921773  0.005
    Value Close To    ${response.json()['altitude']}  300.00000  30.0
    Value Close To    ${response.json()['airspeed']}  30.00000  10.0
    Value Close To    ${response.json()['heading']}   45.00000  10.0
    Value Close To    ${response.json()['roll']}  0.0  5.0
    Value Close To    ${response.json()['pitch']}  0.0  5.0

Get Engine Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/engine
    [Return]    ${resp}

Should Be Valid Engine Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  thrust
    JSON Response Should Contain item    ${response}  throttle

Should Be Valid Engine Response With Engine On Idle
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['throttle']}  0.0

Get The Flight Controls Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/controls
    [Return]    ${resp}

Should Be Valid Flight Control Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  aileron
    JSON Response Should Contain item    ${response}  elevator
    JSON Response Should Contain item    ${response}  rudder
    JSON Response Should Contain item    ${response}  throttle

Should be Valid Flight Controls Response With Flight Controls Idle
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['aileron']}  0.0
    Should Be Equal As Numbers    ${response.json()['elevator']}  0.0
    Should Be Equal As Numbers    ${response.json()['rudder']}  0.0
    Should Be Equal As Numbers    ${response.json()['throttle']}  0.0

Run Simulator For
    [Arguments]    ${session}    ${run_for}
    ${command_data} =    Create Dictionary  command=${command}  run_for=${run_for}
    ${headers}=  Create Dictionary  Content-Type=application/json
    ${resp} =    Post Request    huginn_web_server  /simulator  data=${command_data}  headers=${headers}
    [Return]    ${resp}

Get FDM Accelerations Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm/accelerations
    [Return]    ${resp}

Is Valid FDM Accelerations Data Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  x
    JSON Response Should Contain item    ${response}  y
    JSON Response Should Contain item    ${response}  z
    JSON Response Should Contain item    ${response}  u_dot
    JSON Response Should Contain item    ${response}  v_dot
    JSON Response Should Contain item    ${response}  w_dot
    JSON Response Should Contain item    ${response}  p_dot
    JSON Response Should Contain item    ${response}  q_dot
    JSON Response Should Contain item    ${response}  r_dot
    JSON Response Should Contain item    ${response}  gravity

Is FDM accelerations Data Response With Aircraft In The Start Location
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['x']}  ${IC_X_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['y']}  ${IC_Y_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['z']}  ${IC_Z_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['u_dot']}  ${IC_U_DOT}  precision=4
    Should Be Equal As Numbers    ${response.json()['v_dot']}  ${IC_V_DOT}  precision=4
    Should Be Equal As Numbers    ${response.json()['w_dot']}  ${IC_W_DOT}  precision=4
    Should Be Equal As Numbers    ${response.json()['p_dot']}  ${IC_P_DOT}  precision=4
    Should Be Equal As Numbers    ${response.json()['q_dot']}  ${IC_Q_DOT}  precision=4
    Should Be Equal As Numbers    ${response.json()['r_dot']}  ${IC_R_DOT}  precision=4
    Should Be Equal As Numbers    ${response.json()['gravity']}  ${IC_GRAVITY}  precision=4

Get FDM Velocity Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm/velocities
    [Return]    ${resp}

Is Valid FDM Velocity Data Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  p
    JSON Response Should Contain item    ${response}  q
    JSON Response Should Contain item    ${response}  r
    JSON Response Should Contain item    ${response}  true_airspeed
    JSON Response Should Contain item    ${response}  climb_rate
    JSON Response Should Contain item    ${response}  u
    JSON Response Should Contain item    ${response}  v
    JSON Response Should Contain item    ${response}  w
    JSON Response Should Contain item    ${response}  calibrated_airspeed
    JSON Response Should Contain item    ${response}  equivalent_airspeed
    JSON Response Should Contain item    ${response}  ground_speed

Is FDM Velocity Data Response With Aircraft In The Start Location
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['p']}  ${IC_P}  precision=4
    Should Be Equal As Numbers    ${response.json()['q']}  ${IC_Q}  precision=4
    Should Be Equal As Numbers    ${response.json()['r']}  ${IC_R}  precision=4
    Should Be Equal As Numbers    ${response.json()['true_airspeed']}  ${IC_AIRSPEED}  precision=4
    Should Be Equal As Numbers    ${response.json()['climb_rate']}  ${IC_CLIMB_RATE}  precision=4
    Should Be Equal As Numbers    ${response.json()['u']}  ${IC_U}  precision=4
    Should Be Equal As Numbers    ${response.json()['v']}  ${IC_V}  precision=4
    Should Be Equal As Numbers    ${response.json()['w']}  ${IC_W}  precision=4
    Should Be Equal As Numbers    ${response.json()['calibrated_airspeed']}  ${IC_CALIBRATED_AIRSPEED}  precision=4
    Should Be Equal As Numbers    ${response.json()['equivalent_airspeed']}  ${IC_EQUIVALENT_AIRSPEED}  precision=4
    Should Be Equal As Numbers    ${response.json()['ground_speed']}  ${IC_GROUND_SPEED}  precision=4

Get FDM Orientation Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm/orientation
    [Return]    ${resp}

Is Valid FDM Orientation Data Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  phi
    JSON Response Should Contain item    ${response}  theta
    JSON Response Should Contain item    ${response}  psi

Is FDM Orientation Data Response With Aircraft In The Start Location
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['phi']}  ${IC_PHI}  precision=4
    Should Be Equal As Numbers    ${response.json()['theta']}  ${IC_THETA}  precision=4
    Should Be Equal As Numbers    ${response.json()['psi']}  ${IC_PSI}  precision=4
