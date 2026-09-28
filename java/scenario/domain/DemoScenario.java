package com.ruoyi.scenario.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 云场景对象 demo_scenario
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
public class DemoScenario extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 场景ID（主键，自动递增） */
    private Long sceId;

    /** 机构ID */
    @Excel(name = "机构ID")
    private Long orgId;

    /** 机构名称 */
    @Excel(name = "机构名称")
    private String orgName;


    /** 场景主标题 */
    @Excel(name = "场景主标题")
    private String sceMainTitle;

    /** 场景副标题 */
    @Excel(name = "场景副标题")
    private String sceSubTitle;

    /** 场景标签 */
    @Excel(name = "场景标签")
    private String sceTag;

    /** 场景图片URL */
    @Excel(name = "场景图片URL")
    private String sceImgUrl;

    /** 场景内容 */
    private String sceContent;

    /** 阅读量 */
    private Long sceReads;

    /** 点赞量 */
    private Long sceLikes;

    /** 分享量 */
    private Long sceShares;

    /** 场景状态 */
    @Excel(name = "场景状态")
    private String sceStatus;

    /** 审核用户ID */
    private Long sceApprovedUserId;

    /** 审核时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "审核时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date sceApprovedTime;

    /** 未通过原因 */
    private String sceUnapprovedReason;

    /** 创建用户ID */
    private Long createUserId;

    public void setSceId(Long sceId) 
    {
        this.sceId = sceId;
    }

    public Long getSceId() 
    {
        return sceId;
    }

    public void setOrgId(Long orgId) 
    {
        this.orgId = orgId;
    }

    public Long getOrgId() 
    {
        return orgId;
    }

    public void setOrgName(String orgName) 
    {
        this.orgName = orgName;
    }

    public String getOrgName() 
    {
        return orgName;
    }

    public void setSceMainTitle(String sceMainTitle) 
    {
        this.sceMainTitle = sceMainTitle;
    }

    public String getSceMainTitle() 
    {
        return sceMainTitle;
    }

    public void setSceSubTitle(String sceSubTitle) 
    {
        this.sceSubTitle = sceSubTitle;
    }

    public String getSceSubTitle() 
    {
        return sceSubTitle;
    }

    public void setSceTag(String sceTag) 
    {
        this.sceTag = sceTag;
    }

    public String getSceTag() 
    {
        return sceTag;
    }

    public void setSceImgUrl(String sceImgUrl) 
    {
        this.sceImgUrl = sceImgUrl;
    }

    public String getSceImgUrl() 
    {
        return sceImgUrl;
    }

    public void setSceContent(String sceContent) 
    {
        this.sceContent = sceContent;
    }

    public String getSceContent() 
    {
        return sceContent;
    }

    public void setSceReads(Long sceReads) 
    {
        this.sceReads = sceReads;
    }

    public Long getSceReads() 
    {
        return sceReads;
    }

    public void setSceLikes(Long sceLikes) 
    {
        this.sceLikes = sceLikes;
    }

    public Long getSceLikes() 
    {
        return sceLikes;
    }

    public void setSceShares(Long sceShares) 
    {
        this.sceShares = sceShares;
    }

    public Long getSceShares() 
    {
        return sceShares;
    }

    public void setSceStatus(String sceStatus) 
    {
        this.sceStatus = sceStatus;
    }

    public String getSceStatus() 
    {
        return sceStatus;
    }

    public void setSceApprovedUserId(Long sceApprovedUserId) 
    {
        this.sceApprovedUserId = sceApprovedUserId;
    }

    public Long getSceApprovedUserId() 
    {
        return sceApprovedUserId;
    }

    public void setSceApprovedTime(Date sceApprovedTime) 
    {
        this.sceApprovedTime = sceApprovedTime;
    }

    public Date getSceApprovedTime() 
    {
        return sceApprovedTime;
    }

    public void setSceUnapprovedReason(String sceUnapprovedReason) 
    {
        this.sceUnapprovedReason = sceUnapprovedReason;
    }

    public String getSceUnapprovedReason() 
    {
        return sceUnapprovedReason;
    }

    public void setCreateUserId(Long createUserId) 
    {
        this.createUserId = createUserId;
    }

    public Long getCreateUserId() 
    {
        return createUserId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("sceId", getSceId())
            .append("orgId", getOrgId())
            .append("sceMainTitle", getSceMainTitle())
            .append("sceSubTitle", getSceSubTitle())
            .append("sceTag", getSceTag())
            .append("sceImgUrl", getSceImgUrl())
            .append("sceContent", getSceContent())
            .append("sceReads", getSceReads())
            .append("sceLikes", getSceLikes())
            .append("sceShares", getSceShares())
            .append("sceStatus", getSceStatus())
            .append("sceApprovedUserId", getSceApprovedUserId())
            .append("sceApprovedTime", getSceApprovedTime())
            .append("sceUnapprovedReason", getSceUnapprovedReason())
            .append("createUserId", getCreateUserId())
            .append("createTime", getCreateTime())
            .append("updateTime", getUpdateTime())
            .toString();
    }
}
