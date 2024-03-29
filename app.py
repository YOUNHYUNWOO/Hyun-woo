# 필요한 라이브러리를 불러온다.
import streamlit as st
from PIL import Image
import os

# 배경(background) thmeme 적용
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url(https://i.imgur.com/jDFbAfg.png);
             background-attachment: fixed;
             background-size: cover;       
         }}
         </style>
         """,
         unsafe_allow_html=True
    )
add_bg_from_url()

# 이미지들을 가로로 결합하는 함수
def concatenate_images(images):
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    combined_image = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))

    x_offset = 0
    for img in images:
        img = img.convert("RGBA") # 이미지를 RGBA 형식으로 변환
        combined_image.paste(img, (x_offset, 0), mask=img)
        x_offset += img.width

    return combined_image

# 이미지에 스타일을 적용하는 함수
@st.cache_data
def apply_style_to_directory(original_images_directory, style_image_path):
    style_image = Image.open(style_image_path)
    
    for filename in os.listdir(original_images_directory):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(original_images_directory, filename)
            try:
                original_image = Image.open(file_path)
                resized_image = original_image.resize(style_image.size)
                resized_image.save(file_path)
                
            except IOError:
                print(f"Error processing {file_path}")

# 메인 함수
def main():
    # title 제목
    st.markdown("<h1 style='text-align: center; color:white;'>GIF 생성 과정</h1>", unsafe_allow_html=True)
    
    # 이미지 저장 경로
    original_images_directory = r"Test_folder\frames"
    style_image_path = r"Test_folder\Picasso-The_Weeping_Woman.jpg"
    composite_images_directory = r"Test_folder\transferred_images"
    gif_path = r"Test_folder\Jay-won.gif"


    # 사이드바 버튼을 가운데 정렬로 배열하기
    st.markdown(
    """
    <style>
    
    .stButton {
        width: 500px; /* 원하는 크기로 조정 */
        height: 50px; /* 원하는 크기로 조정 */
        display : flex;
        justify-content: center;
        align-items: center;              
    }
    </style>
    """,
    unsafe_allow_html=True)
    
    # 사이드바 과정 1 ~ 3까지 설명
    if st.sidebar.button('과정1'):
        apply_style_to_directory(original_images_directory, style_image_path)
        
        filenames = [f for f in os.listdir(original_images_directory) if f.endswith((".png", ".jpg", ".jpeg"))]
        if filenames:
            first_image_path = os.path.join(original_images_directory, filenames[0])
            original_image_to_show = Image.open(first_image_path)
            style_image_to_show = Image.open(style_image_path)
            
            # 원본 이미지와 스타일 이미지를 나란히 표시합니다.
            st.write("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.image([original_image_to_show, style_image_to_show], caption=["X_original", "X_style"], width=350)
            st.write("</div>", unsafe_allow_html=True)
            
            #추가로 이미지를 설명하는 텍스트 작성
            st.write("<div style='text-align: center; color:white; font-size: 20px;'>해당 X_original(원본)와 X_style(스타일)을 보여준다.</div>", unsafe_allow_html=True)
        
        else:
            st.write("디렉토리에 이미지 파일이 없습니다.")
    
    
    if st.sidebar.button('과정2'):
        # filenames 변수 정의
        filenames = [f"frame_{i}.png" for i in range(80)]  # frame_0.png부터 frame_81.png까지 

        if filenames:
            # 원본 이미지들을 추가합니다. 
            original_images_to_show = []
            original_captions = []
            for filename in filenames:
                image_path = os.path.join(original_images_directory, filename)
                original_images_to_show.append(Image.open(image_path))
                original_captions.append("원본 이미지: " + filename)

            # 합성된 이미지들을 추가합니다.
            composite_images_to_show = []
            composite_captions = []
            for i in range(79):    # 합성이미지_0.png ~ 합성이미지_78.png
                composite_filename = f"합성 이미지_{i}.png"
                composite_image_path = os.path.join(composite_images_directory, composite_filename)
                if os.path.isfile(composite_image_path):
                    composite_images_to_show.append(Image.open(composite_image_path))
                    composite_captions.append(f"합성된 이미지 {i}")

            # 이미지와 텍스트를 가로 일렬로 배열하여 표시
            num_images = min(len(original_images_to_show), len(composite_images_to_show), 10) # 최대 10개        

            # 이미지를 가로로 결합하여 표시
            st.image(concatenate_images(original_images_to_show[:num_images]), caption="X_original", width=700)
            st.write("...")
            st.write("<div style='text-align: center; font-size: 80px;'> + </div>", unsafe_allow_html=True)
            st.image(concatenate_images(composite_images_to_show[:num_images]), caption="transferred_images", width=700)
            st.write("...")
            if len(original_images_to_show) > 10 or len(composite_images_to_show) > 10:
              
                
                # 추가로 이미지를 설명하는 텍스트를 입력
                st.write("<div style='text-align: center; color:white; font-size: 20px;'>원본 이미지들과 합성된 이미지들을 합치면 어떤 결과가 나올것인가?</div>", unsafe_allow_html=True)
        else:
            st.write("디렉토리에 이미지 파일이 없습니다.")
        
      
    if st.sidebar.button('과정3'):
        # GIF 파일을 표시합니다.
        if os.path.isfile(gif_path):
            # st.columns를 사용하여 이미지를 중앙에 배치합니다.
            col1, col2, col3 = st.columns([1,2,1])  # 중앙 열에 더 큰 가중치를 부여합니다.
        
        with col2:  # 이미지를 중앙 열에 표시합니다.
            st.image(gif_path, caption="Jay-won.gif", width=350)
    else:
        pass  # 파일이 없을 대 사용자에게 메시지를 보여주고 싶지 않을때

if __name__ == "__main__":
    main()  