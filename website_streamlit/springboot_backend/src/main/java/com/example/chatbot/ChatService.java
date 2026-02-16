package com.example.chatbot;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class ChatService {

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    @Value("${openai.api.key}")
    private String openAiApiKey;

    public ChatService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl("https://api.openai.com/v1").build();
        this.objectMapper = new ObjectMapper();
    }

    public String getChatReply(String message) {
        try {
            OpenAIRequest payload = new OpenAIRequest(
                "gpt-3.5-turbo",
                new Message[] {
                    new Message("system", "You are a helpful assistant in the sector of finance and investments."),
                    new Message("user", message)
                }
            );

            String response = webClient.post()
                .uri("/chat/completions")
                .header("Authorization", "Bearer " + openAiApiKey)
                .header("Content-Type", "application/json")
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(String.class)
                .block();

            // Parse the JSON response to extract the message content
            JsonNode jsonNode = objectMapper.readTree(response);
            String reply = jsonNode
                .path("choices")
                .get(0)
                .path("message")
                .path("content")
                .asText();
            
            return reply;
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    public static class OpenAIRequest {
        private String model;
        private Message[] messages;

        public OpenAIRequest(String model, Message[] messages) {
            this.model = model;
            this.messages = messages;
        }

        // Required for Jackson serialization
        public OpenAIRequest() {
        }

        public String getModel() {
            return model;
        }

        public void setModel(String model) {
            this.model = model;
        }

        public Message[] getMessages() {
            return messages;
        }

        public void setMessages(Message[] messages) {
            this.messages = messages;
        }
    }

    public static class Message {
        private String role;
        private String content;

        public Message(String role, String content) {
            this.role = role;
            this.content = content;
        }

        // Required for Jackson serialization
        public Message() {
        }

        public String getRole() {
            return role;
        }

        public void setRole(String role) {
            this.role = role;
        }

        public String getContent() {
            return content;
        }

        public void setContent(String content) {
            this.content = content;
        }
    }
}
