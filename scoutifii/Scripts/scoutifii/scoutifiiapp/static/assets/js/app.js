
        /*.........Swiper............*/

        let swiper = new Swiper(".mySwiper", {
            slidesPerView: 6,
            spaceBetween: 1,
        });

         /*Windows scroll  */
        window.addEventListener('scroll', ()=>{
            document.querySelector('.profile-popup').style.display = 'none';
            document.querySelector('.add-post-popup').style.display = 'none';
            document.querySelector('.notification-box').style.display = 'none';
        });

        // Sidebar
        const menuItems = document.querySelectorAll('.menu-item');

        const removeActiveItem = () => {
            menuItems.forEach(item =>{
                item.classList.remove('active');
            })
        }

        menuItems.forEach(item =>{
           item.addEventListener('click', () => { 
                removeActiveItem();
                item.classList.add('active');
            })  
        })



        // Active class remove
       const removeActive = ()=>{
            menuItem.forEach(item=>{
                item.classList.remove('active');
            });
        }

        // start aside -->
       let menuItem =  document.querySelectorAll('.menu-item');

       menuItem.forEach(item=>{
            item.addEventListener('click', ()=>{
                removeActive();
                item.classList.add('active');
                document.querySelector('.notification-box').style.display = 'none';
            });
       });

       // ...................Notifications ...................
       document.querySelector('#Notify-box').addEventListener('click', ()=>{
            document.querySelector('.notification-box').style.display = 'block';
            document.querySelector('#ntCounter1').style.display = 'none';
       });

       // ..................Messages........................
       document.querySelector('#messageMenu').addEventListener('click', ()=>{
            document.querySelector('#notifyCounter2').style.display = 'none';
            document.querySelector('.messages').classList.toggle('boxshadow1');
            setTimeout(()=>{
                document.querySelector('.messages').classList.remove('boxshadow1');
            }, 300);
       });

        document.querySelectorAll("#my-profile-picture").forEach(AllProfile => {
            AllProfile.addEventListener('click', ()=>{
                document.querySelector('.profile-popup').style.display = 'flex';
            })
        });
        document.querySelectorAll('.close').forEach(AllCloser =>{
            AllCloser.addEventListener('click', ()=>{
                document.querySelector('.profile-popup').style.display = 'none';
                document.querySelector('.add-post-popup').style.display = 'none';
            })
        });
        document.querySelector('#profile-upload').addEventListener('change', ()=>{
            document.querySelectorAll('#my-profile-picture img').forEach(AllMyProfileImg=>{
                AllMyProfileImg.src = URL.createObjectURL(document.querySelector('#profile-upload').files[0])
            })
        });


        document.querySelector('#crate-lg').addEventListener('click', ()=>{
            document.querySelector('.add-post-popup').style.display = 'flex';
        });

        document.querySelector('#feed-pic-upload').addEventListener('change', ()=>{
            document.querySelector('#postImg').src = URL.createObjectURL(document.querySelector('#feed-pic-upload').files[0])
        });


        document.querySelector('#add-story').addEventListener('change', ()=>{
            document.querySelector('.story img').src = URL.createObjectURL(document.querySelector('#add-story').files[0]);
            document.querySelector('.add-story').style.display = 'none';
        });

        document.querySelector('.mini-button').addEventListener('click', ()=>{
            document.querySelector('.input-post').classList.toggle('boxshadow1');
            setTimeout(()=>{
                document.querySelector('.input-post').classList.remove('boxshadow1');
            }, 300);
        });

        document.querySelector('.mini-button').addEventListener('dblclick', ()=>{
            document.querySelector('.add-post-popup').style.display = 'flex';
        });

        /*setTimeout(()=>{
            document.querySelector('.input-post').classList.remove('boxhadow1');
            document.querySelector('.messages').classList.remove('boxshadow1');
        }, 300);*/

        //--------Liked Button----------->
        document.querySelectorAll('.action-button span:first-child svg').forEach(liked=>{
            liked.addEventListener('click', ()=>{
                liked.classList.toggle('liked');
            });
        });

        // ............Friend Request....................
        let Accept = document.querySelectorAll('#accept');
        let Decline = document.querySelectorAll('#decline');

        Accept.forEach(accept=>{
            accept.addEventListener('click', ()=>{
                accept.parentElement.style.display = 'none';
                accept.parentElement.parentElement.querySelector('.alert').style.display='block';
            });
        });
        Decline.forEach(decline=>{
            decline.addEventListener('click', ()=>{
                decline.parentElement.parentElement.style.display = 'none';
            });
        });


        //.....................Emojis........................
        const emojiBtn = document.querySelector('#emoji-button');

        const picker = new EmojiButton();

        emojiBtn.addEventListener('click', (e) => {
            e.preventDefault();
            picker.togglePicker(emojiBtn);        
        });

        picker.on('emoji', emoji => {
            document.querySelector('#add-comment').value += emoji;
        });

        const comments = document.querySelector('#comments-link');
        document.querySelector('#comments-link').addEventListener('click', ()=>{
            if(comments.style.display === "none"){
                document.querySelector('.input-comment').style.display = 'flex';
            } else{
            document.querySelector('.input-comment').style.display = 'none';
        }
        });

        // Video download
        document.querySelector('#download_video').addEventListener('click', ()=>{
            this.href = document.querySelector('#video_canvas').toDataURL();
            this.download = 'video.jpg';
        });

        // File uploads
        document.querySelector("#add-post").addEventListener('change', (e)=>{
            e.preventDefault();
            const url = $(this).attr('action');
            $.ajax({
                type: 'POST',
                url: 'url',
                data: new FormData(this),
                contentType: false,
                cache: false,
                processData: false,
                success: function(){
                    toastr.success("uploaded");
                    window.location.reload('');
                },
                xhr: function(){
                    let xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener("progress", (e)=>{
                        if(e.lengthComputable){
                            let percent = Math.round(((e.loaded/e.total) * 100));
                            document.querySelector("#progress-bar").style.display = 'block';
                            document.querySelector("#progress-bar-process").style.width = ""+percent+'%';
                            document.querySelector("#progress-bar-process").innerHTML = ""+percent+'% completed';
                            document.querySelector("#uploaded-video").innerHTML = "Uploaded:" + parseInt(e.loaded/1000000)+"/"+parseInt(e.total/1000000)+"MB";

                        }
                    }, false);
                    xhr.addEventListener("load", ()=>{
                        document.querySelector("#progress-bar").value = '';
                    });
                    return xhr;
                },
                error: function(error){
                    toastr.error("error");
                },
            });
            return false;
        });


        //..............MESSAGES.....................
        // searches chats
        const messages = document.querySelector('.messages');
        const message = document.querySelectorAll('.message');
        const messageSearch = document.querySelector('#message-search');

        const searchMessage = () => {
            const val = messageSearch.value.toLowerCase();
            message.forEach(chat => {
                let name = chat.querySelector('h5').textContent.toLowerCase();
                if(name.indexOf(val) != -1){
                    chat.style.display = 'flex';
                } else{
                    chat.style.display = 'none';
                }
            })

        }
        messageSearch.addEventListener('keyup', searchMessage);

    // THEME CUSTOMIZATION
        const theme = document.querySelector('#theme');
        const themeModal = document.querySelector('.customize-theme');
        const fontSizes = document.querySelectorAll('.choose-size span');
        const root = document.querySelector(':root');
        const colorPalette = document.querySelectorAll('.choose-color span');
        const Bg1 = document.querySelector('.bg-1');
        const Bg2 = document.querySelector('.bg-2');
        const Bg3 = document.querySelector('.bg-3');

        //opens modal
        const openThemeModal = () =>{
            themeModal.style.display = 'grid';
        }

        //closes modal
        const closeThemeModal = (e) =>{
            if(e.target.classList.contains('customize-theme')){
                themeModal.style.display = 'none';
            }
        }

        theme.addEventListener('click', openThemeModal);
        themeModal.addEventListener('click', closeThemeModal);

        // remove active class from spans or font size selectors
        const removeSizeSelector = () => {
            fontSizes.forEach(size => {
                size.classList.remove('active');
            })
        }

        // FONTS
         fontSizes.forEach(size => {
            size.addEventListener('click', () => {
                removeSizeSelector()
                let fontsize;
                size.classList.toggle('active');
                if(size.classList.contains('font-size-1')){
                    fontsize = '10px';
                    root.style.setProperty('----sticky-top-left', '5.4rem');
                    root.style.setProperty('----sticky-top-right', '5.4rem');
                } else if(size.classList.contains('font-size-2')){
                    fontsize = '13px';
                    root.style.setProperty('----sticky-top-left', '5.4rem');
                    root.style.setProperty('----sticky-top-right', '-7rem');
                } else if(size.classList.contains('font-size-3')){
                    fontsize = '15px';
                    root.style.setProperty('----sticky-top-left', '-2rem');
                    root.style.setProperty('----sticky-top-right', '-17rem');
                } else if(size.classList.contains('font-size-4')){
                    fontsize = '17px';
                    root.style.setProperty('----sticky-top-left', '5rem');
                    root.style.setProperty('----sticky-top-right', '-25rem');
                } else if(size.classList.contains('font-size-5')){
                    fontsize = '19px';
                    root.style.setProperty('----sticky-top-left', '-12rem');
                    root.style.setProperty('----sticky-top-right', '-33rem');
                }
                // change font sizes of html root element
                document.querySelector('html').style.fontSize = fontsize;
            })
         })

         // Remobe active class from colors
         const changeActiveColorClass = () => {
            colorPalette.forEach(colorPicker =>{
                colorPicker.classList.remove('active')
            })
         }

         //CHANGE COLOR BACKGROUND
         colorPalette.forEach(color =>{
            color.addEventListener('click', () => {
                let primary;
                changeActiveColorClass();
                if(color.classList.contains('color-1')){
                    primaryHue = 52;
                } else if(color.classList.contains('color-2')){
                    primaryHue = 252;
                } else if(color.classList.contains('color-3')){
                    primaryHue = 352;
                } else if(color.classList.contains('color-4')){
                    primaryHue = 152;
                } else if(color.classList.contains('color-5')){
                    primaryHue = 202;
                }
                color.classList.add('active')
                root.style.setProperty('--color-primary-hue', primaryHue)
            });
         })

         // theme background values
         let whiteColorLightness;
         let lightColorLightness;
         let darkColorLightness;

         // changes background color
         const changeBG = () =>{
            root.style.setProperty('--color-light-lightness', lightColorLightness);
            root.style.setProperty('--color-white-lightness', whiteColorLightness);
            root.style.setProperty('--color-dark-lightness', darkColorLightness);
         }

         Bg1.addEventListener('click', () =>{
            darkColorLightness = '252';
            whiteColorLightness = '100%';
            lightColorLightness = '90%';

            Bg1.classList.add('active');
            Bg2.classList.remove('active');
            Bg3.classList.remove('active');
            //remove customized changes from local storage
            //window.location.reload();
            changeBG();
         });

         Bg2.addEventListener('click', () =>{
            darkColorLightness = '95%';
            whiteColorLightness = '20%';
            lightColorLightness = '15%';

            Bg2.classList.add('active');
            Bg1.classList.remove('active');
            Bg3.classList.remove('active');
            changeBG();
         });

         Bg3.addEventListener('click', () =>{
            darkColorLightness = '95%';
            whiteColorLightness = '10%';
            lightColorLightness = '0%';

            Bg3.classList.add('active');
            Bg1.classList.remove('active');
            Bg2.classList.remove('active');
            changeBG();
         });
