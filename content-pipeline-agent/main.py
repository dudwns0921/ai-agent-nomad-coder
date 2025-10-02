from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel
from crewai.agent import Agent
from tools import web_search_tool
from crewai.llm import LLM
from seo_crew import SeoCrew
from virality_crew import ViralityCrew


class BlogPost(BaseModel):
    title: str
    content: str
    sections: list[str]


class Tweet(BaseModel):
    content: str
    hashtags: list[str]


class LinkedInPost(BaseModel):
    hook: str
    content: str
    call_to_action: str


class Score(BaseModel):
    score: int
    reason: str


class ContentPipelineFlowState(BaseModel):
    # Inputs
    content_type: str = ""
    topic: str = ""

    # Internal
    max_characters: int = 500
    score: Score | None = None
    research: str = ""

    # Content
    blog_post: BlogPost | None = None
    tweet: Tweet | None = None
    linkedin_post: LinkedInPost | None = None


class ContentPipelineFlow(Flow[ContentPipelineFlowState]):
    def _generate_content(self, content_type: str, model_class, existing_content=None):
        """공통 콘텐츠 생성 로직"""
        llm = LLM("openai/o4-mini", response_format=model_class)

        if existing_content is None:
            # 새로운 콘텐츠 생성
            if content_type == "blog":
                prompt = f"""Create a comprehensive blog post about {self.state.topic}.
                Requirements:
                - Write in an engaging, informative tone
                - Include relevant examples and insights
                - Structure with clear headings and subheadings
                - Target length: approximately {self.state.max_characters} characters
                - Make it SEO-friendly with natural keyword integration

                Research Material:
                <research>
                {self.state.research}
                </research>

                Please create a well-structured blog post based on the research above."""

            elif content_type == "tweet":
                prompt = f"""Create an engaging tweet about {self.state.topic}.
                Requirements:
                - Must be under {self.state.max_characters} characters
                - Include relevant hashtags
                - Be concise and impactful
                - Encourage engagement (likes, retweets, replies)
                - Use a conversational tone

                Research Material:
                <research>
                {self.state.research}
                </research>

                Please create a compelling tweet based on the research above."""

            elif content_type == "linkedIn post":
                prompt = f"""Create a professional LinkedIn post about {self.state.topic}.
                Requirements:
                - Professional yet engaging tone
                - Include a compelling hook
                - Structure with clear sections
                - Target length: approximately {self.state.max_characters} characters
                - Include a strong call-to-action
                - Encourage professional networking and discussion

                Research Material:
                <research>
                {self.state.research}
                </research>

                Please create a professional LinkedIn post based on the research above."""
        else:
            # 기존 콘텐츠 개선
            if content_type == "blog":
                prompt = f"""Improve the following blog post to enhance its SEO performance.
                It does not have good SEO right now because of {self.state.score.reason}.
                Current Blog Post:
                <blog_post>
                {existing_content}
                </blog_post>

                Additional Research:
                <research>
                {self.state.research}
                </research>

                SEO Improvement Guidelines:
                - Optimize title and headings with relevant keywords
                - Improve content structure and readability
                - Add internal linking opportunities where appropriate
                - Enhance meta description appeal
                - Maintain the original voice and key messages
                - Keep length around {self.state.max_characters} characters

                Please provide the improved version."""

            elif content_type == "tweet":
                prompt = f"""Improve the following tweet to enhance its virality potential.
                It does not have good virality right now because of {self.state.score.reason}.
                Current Tweet:
                <tweet>
                {existing_content}
                </tweet>

                Additional Research:
                <research>
                {self.state.research}
                </research>

                Virality Improvement Guidelines:
                - Make it more engaging and shareable
                - Optimize hashtags for better reach
                - Improve call-to-action
                - Make it more relatable or controversial (within reason)
                - Keep under {self.state.max_characters} characters

                Please provide the improved version."""

            elif content_type == "linkedIn post":
                prompt = f"""Improve the following LinkedIn post to enhance its professional engagement.
                It does not have good engagement right now because of {self.state.score.reason}.
                Current LinkedIn Post:
                <linkedin_post>
                {existing_content}
                </linkedin_post>

                Additional Research:
                <research>
                {self.state.research}
                </research>

                Engagement Improvement Guidelines:
                - Strengthen the hook to grab attention
                - Improve professional storytelling
                - Enhance call-to-action for better engagement
                - Make it more valuable for professional audience
                - Keep length around {self.state.max_characters} characters

                Please provide the improved version."""

        return llm.call(prompt)

    @start()
    def init_content_pipeline(self):
        print("Initializing content pipeline...")
        print(self.state)
        if self.state.content_type not in ["tweet", "blog", "linkedIn post"]:
            raise ValueError("content_type must be one of: tweet, blog, linkedIn post")

        if not self.state.topic:
            raise ValueError("topic must be provided")

        if self.state.content_type == "tweet":
            self.state.max_characters = 280
        elif self.state.content_type == "blog":
            self.state.max_characters = 2000
        elif self.state.content_type == "linkedIn post":
            self.state.max_characters = 1300

    @listen(init_content_pipeline)
    def conduct_research(self):
        topic = self.state.topic
        print(f"Researching topic: {topic}")

        researcher = Agent(
            role="Content Research Specialist",
            backstory="""You are an experienced researcher specializing in gathering 
        comprehensive and accurate information on various topics. With years of 
        experience in content research, you excel at finding credible sources, 
        extracting key insights, and synthesizing information into actionable 
        intelligence for content creators.""",
            goal=f"""Conduct thorough research on the {topic} and provide well-organized, 
            credible information that will serve as a foundation for creating high-quality content.""",
            tools=[web_search_tool],
        )

        response = researcher.kickoff(f"Research the topic: {topic}")
        self.state.research = response

        return True

    @router(conduct_research)
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "tweet":
            return "make_tweet"
        elif content_type == "blog":
            return "make_blog"
        elif content_type == "linkedIn post":
            return "make_linkedin_post"

    @listen(or_("make_blog", "remake_blog"))
    def handle_make_blog(self):
        print("Making blog...")
        result = self._generate_content("blog", BlogPost, self.state.blog_post)
        self.state.blog_post = BlogPost.model_validate_json(result)
        print("Generated Blog Post:", self.state.blog_post)
        return True

    @listen(or_("make_tweet", "remake_tweet"))
    def handle_make_tweet(self):
        print("Making tweet...")
        result = self._generate_content("tweet", Tweet, self.state.tweet)
        self.state.tweet = Tweet.model_validate_json(result)
        print("Generated Tweet:", self.state.tweet)
        return True

    @listen(or_("make_linkedin_post", "remake_linkedin_post"))
    def handle_make_linkedin_post(self):
        print("Making LinkedIn post...")
        result = self._generate_content(
            "linkedIn post", LinkedInPost, self.state.linkedin_post
        )
        self.state.linkedin_post = LinkedInPost.model_validate_json(result)
        print("Generated LinkedIn Post:", self.state.linkedin_post)
        return True

    @listen(handle_make_blog)
    def check_seo(self):
        print("Checking SEO...")
        seo_crew = SeoCrew().crew()
        response = seo_crew.kickoff(
            inputs={
                "blog_post": self.state.blog_post.model_dump(),
                "topic": self.state.topic,
            }
        )
        self.state.score = response.pydantic
        print("SEO Score:", self.state.score)
        # Simulate an SEO score
        return True

    @listen(or_(handle_make_linkedin_post, handle_make_tweet))
    def check_virality(self):
        print("Checking virality...")
        # 트윗과 링크드인 포스트의 바이럴리티 점수 시뮬레이션
        virality_crew = ViralityCrew().crew()

        # Pydantic 객체를 딕셔너리로 변환
        content_data = (
            self.state.tweet.model_dump()
            if self.state.tweet
            else self.state.linkedin_post.model_dump()
        )

        response = virality_crew.kickoff(
            inputs={
                "content": content_data,
                "content_type": self.state.content_type,
                "topic": self.state.topic,
            }
        )
        self.state.score = response.pydantic
        print("Virality Score:", self.state.score)
        return True

    @router(or_(check_seo, check_virality))
    def score_router(self):
        score = self.state.score.score
        content_type = self.state.content_type

        if score >= 8:
            return "check_passed"
        else:
            if content_type == "tweet":
                return "remake_tweet"
            elif content_type == "blog":
                return "remake_blog"
            elif content_type == "linkedIn post":
                return "remake_linkedin_post"

    @listen(or_(check_seo, check_virality))
    @listen("check_passed")
    def finialize_content(self):
        print("Finalizing content...")

        return True


flow = ContentPipelineFlow()
flow.plot()
flow.kickoff(
    inputs={
        "content_type": "linkedIn post",
        "topic": "Frontend development trends in 2024",
    }
)
