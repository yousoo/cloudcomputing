INSERT INTO members (username, password, name, email)
VALUES
('kim01', '1234', '김민수', 'kim01@example.com'),
('lee01', '1234', '이서연', 'lee01@example.com'),
('park01', '1234', '박지훈', 'park01@example.com'),
('choi01', '1234', '최유진', 'choi01@example.com'),
('jung01', '1234', '정도윤', 'jung01@example.com');

INSERT INTO board (member_id, title, content, view_count)
VALUES
(1, '첫 번째 게시글입니다', '김민수가 작성한 첫 번째 게시글 내용입니다.', 12),
(1, 'Azure PostgreSQL 실습 후기', 'Azure에서 PostgreSQL 서버를 만들고 DBeaver로 연결해 보았습니다.', 8),
(2, 'DBeaver 연결 성공', '처음에는 어려웠지만 SSL 설정 후 정상적으로 연결되었습니다.', 15),
(2, 'SQL 테이블 생성 연습', 'members 테이블과 board 테이블을 생성하고 관계를 설정했습니다.', 7),
(3, '클라우드 컴퓨팅 수업 정리', '오늘은 Azure 데이터베이스와 GitHub 연동 방법을 학습했습니다.', 20),
(3, '게시판 기능 아이디어', '회원별로 게시글을 작성하고 조회할 수 있는 구조를 만들어 보았습니다.', 5),
(4, 'GitHub에 SQL 파일 올리기', '작성한 SQL 쿼리를 GitHub 저장소에 업로드하는 방법을 연습했습니다.', 11),
(4, '웹서비스 DB 설계', '간단한 회원 테이블과 게시판 테이블의 관계를 이해했습니다.', 9),
(5, 'Python과 PostgreSQL 연결', '다음 단계에서는 Python에서 PostgreSQL에 접속하는 코드를 작성할 예정입니다.', 18),
(5, 'Flask 게시판 프로젝트 준비', 'Azure DB를 이용하여 간단한 Flask 게시판을 만들어 볼 계획입니다.', 13);