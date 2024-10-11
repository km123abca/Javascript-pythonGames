const buildSceneData=()=>{
    let output_map=[];
    let cw=canvas.width,ch=canvas.height;
    for(let map_elem of gameManager.map)
        {
        if(map_elem.sprite_type=="VerticalPipe" )
            {
               output_map.push({"sprite":"wall",
                                "x":map_elem.x,
                                "y":map_elem.y,
                                "width":map_elem.wid,
                                "height":map_elem.hei,
                                "hitboxoffsetx":0,
                                "hitboxoffsety":0,
                                "isHori":false,
                                "canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="HorizontalPipe")
            {
               output_map.push({"sprite":"wall",
                                "x":map_elem.x,
                                "y":map_elem.y,
                                "width":map_elem.wid,
                                "height":map_elem.hei,
                                "hitboxoffsetx":0,
                                "hitboxoffsety":0,
                                "isHori":true,"canvas_width":cw,
                                "canvas_height":ch}); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="entry")
            {
               output_map.push({"sprite":"entryexit_entry",
                                "x":map_elem.x,
                                "y":map_elem.y,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="exit")
            {
               output_map.push({"sprite":"entryexit_exit",
                                "x":map_elem.x,
                                "y":map_elem.y,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="camstopper_left")
            {
               output_map.push({"sprite":"camstopper_left",
                                "x":map_elem.x,
                                "y":map_elem.y,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="camstopper_right")
            {
               output_map.push({"sprite":"camstopper_right",
                                "x":map_elem.x,
                                "y":map_elem.y,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="scright")
            {
               output_map.push({"sprite":"scenechanger_scright",
                                "x":map_elem.x,
                                "y":map_elem.y,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="scleft")
            {
               output_map.push({"sprite":"scenechanger_scleft",
                                "x":map_elem.x,
                                "y":map_elem.y,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }
        else if(map_elem.sprite_type=="Coin" && map_elem.indicatorDesc=="flower")
            {
               output_map.push({"sprite":"flower",
                                "x":map_elem.x,
                                "y":map_elem.y,
                                "width":50,
                                "height":50,"canvas_width":cw,
                                "canvas_height":ch
                                }); 
            }


        }
        const popupWindow = window.open("", "popup", "width=300,height=200");
        popupWindow.document.write(`<p>${JSON.stringify(output_map)}</p>`);
        popupWindow.document.title = "Your Design";
}