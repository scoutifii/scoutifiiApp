const APP_ID = 'cf3600b52a1849aba17cc3d3080275fe'
const CHANNEL = sessionStorage.getItem('channel')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))
let PROFILE = sessionStorage.getItem('profile')

// if (!UID) {
//     UID = String(Math.floor(Math.random() * 10000))
//     sessionStorage.setItem('UID', UID)
// }

let constraints = {
    encoderConfig: {
        width: {min:640, ideal:1920, max:1920},
        height: {min:480, ideal:1080, max:1080},
    },
    audio: true
}

// create Agora client interface for audio and video streaming
const client = AgoraRTC.createClient({ mode: "live", codec: "vp8"});

let localTracks = []
let remoteUsers = {}

let joinRoomInit = async () => {
    client.on('user-published', handleUserJoined)
    client.on('user-unpublished', handleUserLeft)
    try {
       await client.join(APP_ID, CHANNEL, TOKEN, UID); 
    } catch (error) {
        console.error(error)
        window.open("{% url 'dashboard' %}", '_self')
    }
    
    joinAndDisplayLocalStream()
}
let joinAndDisplayLocalStream = async () => {  
    document.querySelector('#room-name').innerText = CHANNEL
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks(constraints)

    let member = await liveStream()

    let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                    <div class="video-player" id="user-${UID}"></div>
                </div>`
    // append player to video streams
    document.querySelector('#video-streams').insertAdjacentHTML('beforeend', player);
    // play local video track
    localTracks[1].play(`user-${UID}`)

    // publish local tracks to channel
    await client.publish(localTracks[0], localTracks[1])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)
    if(mediaType === 'video'){
        let player = document.querySelector(`user-container-${user.uid}`)
        if (player != null) {
            player.remove()
        } 
        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="username-wrapper"><span class="user-name">scoutifii</span></div>
                    <div class="video-player" id="user-${user.uid}"></div>
                </div>`
    // append player to video streams
         document.querySelector('#video-streams').insertAdjacentHTML('beforeend', player);
         user.videoTrack.play(`user-${user.uid}`)
    }
    if(mediaType === 'audio'){
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.querySelector(`#user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    for (const element of localTracks) {
        const localTrack = element
        localTrack.stop();
        localTrack.close();
    }
    await client.leave()
    window.open("{% url 'dashboard' %}", '_self')
}

let toggleCamera = async (e) => {
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor ='#fff'
    } else {
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor ='rgba(255, 80, 80,1)'
    }
}

let toggleMicrophone = async (e) => {
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor ='#fff'
    } else {
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor ='rgba(255, 80, 80,1)'
    }
}

let liveStream = async () => {
    let response = await fetch('live_stream', {
        method: 'POST',
        headers: {
            contentType: 'application/json'
        },
        body: JSON.stringify({'profile':PROFILE, 'channel_name':CHANNEL, 'UID':UID})
    })
    let stream = await response.json()
    return stream
}

joinRoomInit()
document.querySelector('#leave-btn').addEventListener('click', leaveAndRemoveLocalStream);
document.querySelector('#camera-btn').addEventListener('click', toggleCamera);
document.querySelector('#mic-btn').addEventListener('click', toggleMicrophone);
