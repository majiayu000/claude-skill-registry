---
name: magnifiedskillssequencediagrams
description: participant BotFrameworkAdapter
---

```mermaid
sequenceDiagram
    participant BotFrameworkAdapter
    participant JwtTokenValidation
    participant ChannelValidationClass
    Note over ChannelValidationClass: Examples:
    Note over ChannelValidationClass: SkillValidation
    Note over ChannelValidationClass: EmulatorValidation
    Note over ChannelValidationClass: Public Azure ChannelValidation
    Note over ChannelValidationClass: GovernmentChannelValidation
    Note over ChannelValidationClass: EnterpriseChannelValidation
    participant JwtTokenExtractor
    participant OpenIdMetadata
    participant CredentialProvider
    participant AppCredentials

    BotFrameworkAdapter ->> BotFrameworkAdapter: processActivity()
    activate BotFrameworkAdapter
        Note right of BotFrameworkAdapter: Deserialize Activity
        Note right of BotFrameworkAdapter: Get Bearer Token from Auth Header

        BotFrameworkAdapter ->> BotFrameworkAdapter: authenticateRequestInternal()
        activate BotFrameworkAdapter
            BotFrameworkAdapter ->> JwtTokenValidation: authenticateRequest()
            activate JwtTokenValidation
                JwtTokenValidation ->> JwtTokenValidation: validateAuthHeader()
                activate JwtTokenValidation
                    JwtTokenValidation ->> JwtTokenValidation: authenticateToken()
                    activate JwtTokenValidation
                        Note over JwtTokenValidation, JwtTokenExtractor: Validate Token w/auth validations for specified Channel
                        Note over JwtTokenValidation, ChannelValidationClass: Can be done with or w/o service URL
                        alt is Skill Token
                                JwtTokenValidation ->> ChannelValidationClass: SkillValidation.authenticateChannelToken()
                                activate JwtTokenValidation

                            else is Emulator Token
                                JwtTokenValidation ->> ChannelValidationClass: EmulatorValidation.authenticateEmulatorToken()

                            else is Public Azure Channel
                                JwtTokenValidation ->> ChannelValidationClass: ChannelValidation.authenticateChannelToken()

                            else is Government Channel
                                JwtTokenValidation ->> ChannelValidationClass: GovernmentChannelValidation.authenticateChannelToken()

                            else is Enterprise Channel
                                JwtTokenValidation ->> ChannelValidationClass: EnterpriseChannelValidation.authenticateChannelToken()
                        end

                        Note over JwtTokenValidation, JwtTokenExtractor: SkillValidation.isSkillToken() path
                        activate ChannelValidationClass
                            Note over ChannelValidationClass, OpenIdMetadata: Verify Auth header has Bearer Token (JWT)
                            Note over ChannelValidationClass, OpenIdMetadata: Decode JWT (header, payload, signature)

                            ChannelValidationClass ->> ChannelValidationClass: isSkillClaim()
                            activate ChannelValidationClass
                                Note over ChannelValidationClass, JwtTokenExtractor: Assert that we have following claims:
                                Note over ChannelValidationClass, JwtTokenExtractor: "ver" (1.0 or 2.0)
                                Note over ChannelValidationClass, OpenIdMetadata: "aud" (for from Root to Skill, it's Skill's appId)
                                Note over ChannelValidationClass, JwtTokenExtractor: "appId" (v1.0) or "azp" (v2.0)
                                Note over ChannelValidationClass, JwtTokenExtractor: And "appId"/"azp" != "aud"
                                ChannelValidationClass -->> ChannelValidationClass: Return true, using isSkillClaim
                            deactivate ChannelValidationClass
                        ChannelValidationClass -->> JwtTokenValidation: Return true, using isSkillToken
                        deactivate ChannelValidationClass
                        deactivate JwtTokenValidation

                        JwtTokenValidation ->> ChannelValidationClass: SkillValidation.authenticateChannelToken()
                        activate JwtTokenValidation
                        activate ChannelValidationClass
                            Note over ChannelValidationClass, TurnContext: openIdMetadatUrl: "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration" (non-gov't channel)

                            ChannelValidationClass ->> JwtTokenExtractor: new JwtTokenExtractor
                            activate ChannelValidationClass
                            activate JwtTokenExtractor
                                Note over JwtTokenExtractor, Middleware: Get cached OpenIdMetadata doc or create new one
                                JwtTokenExtractor ->> JwtTokenExtractor: getOrAddOpenIdMetadata()
                                JwtTokenExtractor -->> ChannelValidationClass: Return JwtTokenExtractor w/OpenIdMetadata document
                            deactivate JwtTokenExtractor
                            deactivate ChannelValidationClass

                            ChannelValidationClass ->> JwtTokenExtractor: getIdentity() to get ClaimsIdentity
                            activate ChannelValidationClass
                            activate JwtTokenExtractor
                                Note over ChannelValidationClass, OpenIdMetadata: Verify that token was issued by a valid issuer
                                JwtTokenExtractor ->> JwtTokenExtractor: hasAllowedIssuer()

                                JwtTokenExtractor ->> JwtTokenExtractor: validateToken()
                                activate JwtTokenExtractor
                                    Note over JwtTokenExtractor, OpenIdMetadata: Decode Token (header, payload, signature)

                                    JwtTokenExtractor ->> OpenIdMetadata: Get signing key using "kid" from Token header
                                    activate JwtTokenExtractor
                                    activate OpenIdMetadata
                                    OpenIdMetadata -->> JwtTokenExtractor: return IOpenIdMetadataKey
                                    deactivate JwtTokenExtractor
                                    deactivate OpenIdMetadata

                                    Note over JwtTokenExtractor, CredentialProvider: Validate that token was signed w/valid signing keys
                                    Note over JwtTokenExtractor, CredentialProvider: and endorsed, if any endoresments associated with key
                                    Note over JwtTokenExtractor, CredentialProvider: and that valid signing algorithm was used to sign
                                    Note over JwtTokenExtractor, CredentialProvider: Get claims from Token payload

                                    JwtTokenExtractor -->> JwtTokenExtractor: return new ClaimsIdentity created w/claims from payload
                                deactivate JwtTokenExtractor
                                JwtTokenExtractor -->> ChannelValidationClass: return ClaimsIdentity
                            deactivate JwtTokenExtractor
                            deactivate ChannelValidationClass

                            ChannelValidationClass ->> ChannelValidationClass: validateIdentity()
                            activate ChannelValidationClass
                                Note over ChannelValidationClass: Validate that ClaimsIdentity:
                                Note over ChannelValidationClass: isAuthenticated
                                Note over ChannelValidationClass: has "ver" and "aud" claims

                                ChannelValidationClass ->> CredentialProvider: isValidAppId()
                                activate CredentialProvider
                                CredentialProvider -->> ChannelValidationClass: return true
                                deactivate CredentialProvider
                            deactivate ChannelValidationClass

                            ChannelValidationClass -->> JwtTokenValidation: return ClaimsIdentity
                        deactivate ChannelValidationClass
                        JwtTokenValidation -->> JwtTokenValidation: return ClaimsIdentity
                        deactivate JwtTokenValidation
                    deactivate JwtTokenValidation
                deactivate JwtTokenValidation

                Note over JwtTokenValidation, AppCredentials: Add Servive Url's host to Trusted Hosts
                JwtTokenValidation ->> AppCredentials: trustServiceUrl()
                activate AppCredentials
                deactivate AppCredentials

                JwtTokenValidation -->> BotFrameworkAdapter: return ClaimsIdentity
            deactivate JwtTokenValidation
        deactivate BotFrameworkAdapter

        Note over BotFrameworkAdapter: Create TurnContext

        BotFrameworkAdapter ->> BotFrameworkAdapter: createConnectorClientWithIdentity()
        activate BotFrameworkAdapter
            Note over BotFrameworkAdapter, ChannelValidationClass: Set botAppId to "aud" claim (Skill's AppId)
            Note over BotFrameworkAdapter, ChannelValidationClass: Set scope to be the root bot (use root's AppId)

            opt if botAppId and isSkillClaim
                Note over BotFrameworkAdapter, JwtTokenExtractor: Create AppCredentials instance w/correct scope for consumer-skill communication
                BotFrameworkAdapter ->> JwtTokenValidation: getAppIdFromClaims()
                activate BotFrameworkAdapter
                activate JwtTokenValidation
                JwtTokenValidation -->> BotFrameworkAdapter: return RootBot's AppId
                deactivate JwtTokenValidation
                deactivate BotFrameworkAdapter
            end

            alt if OAuthScope in credentials == RootBot's AppId
                Note over BotFrameworkAdapter, JwtTokenExtractor: Do nothing. Credential's scope already configured properly for consumer-skill communcation

                else scope is not RootBot's AppId
                    Note over BotFrameworkAdapter: (OAuthScope defaults to 'https://api.botframework.com')
                    Note over BotFrameworkAdapter: Build new AppCredentials instance
                    BotFrameworkAdapter ->> BotFrameworkAdapter: buildCredentials()
                    activate BotFrameworkAdapter
                        BotFrameworkAdapter ->> CredentialProvider: getAppPassword()
                        activate BotFrameworkAdapter
                        activate CredentialProvider
                            CredentialProvider -->> BotFrameworkAdapter: return Skill's appPassword
                        deactivate BotFrameworkAdapter
                        deactivate CredentialProvider

                        BotFrameworkAdapter -->> BotFrameworkAdapter: return new MicrosoftAppCredentials
                    deactivate BotFrameworkAdapter

                   BotFrameworkAdapter ->> BotFrameworkAdapter: createConnectorClientInternal()
                   activate BotFrameworkAdapter
                        Note over BotFrameworkAdapter, ChannelValidationClass: Create ConnectorClient w/
                        Note over BotFrameworkAdapter, ChannelValidationClass: SkillHostEndpoint as base URI
                        Note over BotFrameworkAdapter, ChannelValidationClass: And has AppCredentials that have Skill's AppId as AppId
                        Note over BotFrameworkAdapter, ChannelValidationClass: and OAuthScope set to RootBot's AppId
                        BotFrameworkAdapter -->> BotFrameworkAdapter: return ConnectorClient
                   deactivate BotFrameworkAdapter
            end
        deactivate BotFrameworkAdapter

        BotFrameworkAdapter ->> TurnContext: Add BotIdentity (ClaimsIdentity), ConnectorClient, BotCallBackHandler to TurnState
        activate BotFrameworkAdapter
        activate TurnContext
            TurnContext -->> BotFrameworkAdapter:
        deactivate TurnContext
        deactivate BotFrameworkAdapter

    deactivate BotFrameworkAdapter
```