    $(".rec_like").click(function () { // .like 버튼을 클릭 감지
        var pk = $(this).attr('name')  //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        $.ajax({ // ajax로 서버와 통신
            type: "POST", // 데이터를 전송하는 방법
            url: "{% url 'recipe:recipe_like' %}", // 통신할 url을 지정
            data: { 'pk': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}' }, // 서버로 데이터 전송시 옵션, pk를 넘겨야 어떤 레시피인지 알 수 있음
            dataType: "json",
            success: function (response) { // 성공
                alert(response.message);
                $("#rec_count-" + pk).html("좋아요&nbsp;" + response.rec_likes_count + "개"); // 좋아요 개수 변경
                if (response.message == "좋아요")
                    //좋아요 눌렀을 때
                    {
                        $('#rec_heart' + pk).attr("class", "fas fa-heart")
                    } else if (response.message == "좋아요 취소")
                    //좋아요 상태에서 다시 눌렀을 때
                    {
                        $('#rec_heart' + pk).attr("class", "far fa-heart")
                    }
            },
            error: function (request, status, error) { // 실패
                alert("로그인이 필요합니다.")
                window.location.replace("/accounts/login/") // 로그인 페이지로 넘어가기
            },
        });
    })
