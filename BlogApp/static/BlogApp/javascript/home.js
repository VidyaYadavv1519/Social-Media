document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach((button) => {
        let liked = false;
        button.addEventListener("click", function () {
            liked = !liked;
            button.classList.toggle("liked", liked);
            const likesCount = button.querySelector(".likes-count");
            likesCount.textContent = liked
                ? parseInt(likesCount.textContent) + 1
                : parseInt(likesCount.textContent) - 1;

            const likeImage = button.querySelector(".like-image");
            likeImage.style.backgroundImage = liked
                ? 'url("{% static "BlogApp/images/like.png" %}")'
                : 'url("{% static "BlogApp/images/unlike.png" %}")';
        });
    });

    const commentButtons = document.querySelectorAll(".comment-button");

    commentButtons.forEach((button) => {
        const commentBox = button.parentElement.parentElement.querySelector(
            ".comment-box"
        );
        let isCommentBoxVisible = false;

        button.addEventListener("click", function () {
            isCommentBoxVisible = !isCommentBoxVisible;
            commentBox.style.maxHeight = isCommentBoxVisible ? "200px" : "0";
            commentBox.style.display = isCommentBoxVisible ? "block" : "none";
        });
    });

    const createVomitButton = document.getElementById("create-vomit-button");

    createVomitButton.addEventListener("click", function () {
        const csrftoken = $("[name=csrfmiddlewaretoken]").val();
        const title = $("#vomit-textarea").val();
        const formData = new FormData($("#create-vomit-form")[0]);
        formData.append("title", title);
        const headers = {
            "X-CSRFToken": csrftoken,
        };

        $.ajax({
            type: "POST",
            url: 'create_vomit',
            headers: headers,
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response);
                $("#create-vomit-form")[0].reset();
            
                const vomitContainer = document.querySelector(".vomits");
                const newVomit = `
                    <div class="vomit">
                        <p>${response.title}</p>
                        <div class="vomit-image">
                            <img src="${response.blog_image_url}" alt="New Vomit Image" width="1000" height="1000">
                        </div>
                        
                        <div class="button-container">
                            <button id="commentButton" class="comment-button">
                                <div class="comment-circle">
                                    <div class="comment-image"></div>
                                </div>
                                <span class="comment-count">0</span>
                            </button>

                            <button id="likeButton" class="like-button">
                                <div class="like-circle">
                                    <div class="like-image"></div>
                                </div>
                                <span class="likes-count">0</span>
                            </button>
                        </div>

                        <!-- Comment input field -->
                        <div id="comment-box" class="comment-box">
                            <div class="text-area-container">
                                <textarea rows="1" placeholder="Write your comment here..."></textarea>
                                <button class="comment-submit">Submit</button>
                            </div>
                        </div>
                    </div>
                `;
            
                // Insert the new vomit at the beginning of the vomit container
                vomitContainer.insertAdjacentHTML("afterbegin", newVomit);
            },
            error: function (error) {
                console.error(error);
            },
        });
    });
});
