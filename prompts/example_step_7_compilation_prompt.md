# TASK

Write text to accompany a short form video clip to be posted to YouTube, LinkedIn, Instagram, Facebook, TikTok, and X.com (fka Twitter). The clip features a snippet of Tad Duval's presentation at the 1/28/2026 AI MASTERCLASS series event on Agentic Systems. Today's date is 2/20/2026 for context. The CTA of this piece of marketing material is to drive sales for the next installment of the AI MASTERCLASS series. The CTA LINK for the next AI MASTERCLASS event happening Friday, February 27th, 2026, from 6pm to 9pm ET in beautiful Wynwood, Miami, Florida can be found below. After generating all of the marketing copy, store the copy into the `Content` table in Airtable. Make sure to include a link to the media in the `Media` column. And make sure to include the original Dropbox link of the media in the `Note` column of the `Content` table.

## CTA LINK

https://luma.com/ai-masterclass

## LINK TO CLIP

{
"url": "https://www.dropbox.com/scl/fi/w7svwsabn0lpwhn9thd8w/clip_1_FINAL.mp4?rlkey=t7lfo5jrbom2gxioer3eb0do9&st=lga5819x&dl=1",
}

## ABOUT THE CLIP

The video is a short vertical video of Tad Duval walking through an example use case of a react agent, i.e., prospecting customers for marketing purposes.

## TRANSCRIPT OF THE CLIP

This is another diagram that shows what an LLM agent is. Right? So you this is you here. Right? You feed in some prompt. So you're in the hospitality sector? Correct. So I think I remember Francisco was was talking about how you were doing, like, prospecting with Clay. So you were, like, look for people online that around this time last year said they they were gonna be coming to Miami. Something something really intricate like that. Right? So you feed it into itself, and then the agent, right, was like, okay. What the agent will be like, whatever you ask it. Right? So, like, for example, search for people who, around this time last year, said that they were coming to Miami online. Right? So maybe they're coming back here again this year. That's got kinda like the hypothesis. And then you can target those people with marketing. Right? So you feed in that prompt, and then the prompt that the agent will be like, okay. Well, you need to search the Internet or, like, go to Twitter and look and, do some search for people who tagged Miami on some of their posts around October. Right? The LLM would tell you to do that, then you have to go and execute some code that does what the agent is telling you to do. And then you come back to the beginning of the for loop. And if the agent has not told you to stop, then you just take the data along with the initial prompt, then you feed all that back in into itself. Then this process just loops over and over again until the agent or the LLM. Right? The LLM is what powers the agent. Until the LLM tells you to stop, at which point you break out. And usually what happens is if this all works, you get the final answer that's related to what you provided as input.

## GENERAL REQUIREMENT

- Make the output natural and impossible to detect as being A.I. generated
- Use spacing and new lines to make the marketing copy easy to read
- Use minimal emojis
- Do NOT bold any text when generating the copy for LinkedIn
- The marketing copy for X.com should NOT have any hashtags
- Make the posts short and succinct

## OUTPUT SCHEMA

Your output should adhere to the following JSON schema

{
"youtube": {
title: string;
description: string;
},
"linkedin": string;
"x_dot_com_post": string;
"instagram_caption": string;
"tiktok_post": string;
"facebook": string;
}

## SEO KEYWORDS

ai, course, masterclass, miami, south, florida, international, learn, network, agentic, systems