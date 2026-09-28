package com.ruoyi.message.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 申请消息管理对象 demo_message
 * 
 * @author ruoyi
 * @date 2026-06-24
 */
public class DemoMessage extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 消息ID */
    private Long msgId;

    /** 用户ID */
    private Long userId;

    /** 用户名 */
    @Excel(name = "用户名")
    private String userName;

    /** 昵称 */
    @Excel(name = "昵称")
    private String nickName;

    /** 手机 */
    @Excel(name = "手机")
    private String phonenumber;

    /** 邮箱 */
    @Excel(name = "邮箱")
    private String email;

    /** 机构ID */
    private Long orgId;

    /** 机构名称 */
    @Excel(name = "机构名称")
    private String orgName;

    /** 消息内容 */
    @Excel(name = "消息内容")
    private String msgContent;

    /** 申请状态 */
    @Excel(name = "申请状态")
    private String msgStatus;

    /** 审核人ID */
    private Long msgApprovedUserId;

    /** 审核时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "审核时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date msgApprovedTime;

    /** 审核不通过原因 */
    private String msgUnapprovedReason;

    public void setMsgId(Long msgId) 
    {
        this.msgId = msgId;
    }

    public Long getMsgId() 
    {
        return msgId;
    }

    public void setUserId(Long userId) 
    {
        this.userId = userId;
    }

    public Long getUserId() 
    {
        return userId;
    }

    public void setUserName(String userName) 
    {
        this.userName = userName;
    }

    public String getUserName() 
    {
        return userName;
    }

    public void setNickName(String nickName) 
    {
        this.nickName = nickName;
    }

    public String getNickName() 
    {
        return nickName;
    }

    public void setPhonenumber(String phonenumber) 
    {
        this.phonenumber = phonenumber;
    }

    public String getPhonenumber() 
    {
        return phonenumber;
    }

    public void setEmail(String email) 
    {
        this.email = email;
    }

    public String getEmail() 
    {
        return email;
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

    public void setMsgContent(String msgContent) 
    {
        this.msgContent = msgContent;
    }

    public String getMsgContent() 
    {
        return msgContent;
    }

    public void setMsgStatus(String msgStatus) 
    {
        this.msgStatus = msgStatus;
    }

    public String getMsgStatus() 
    {
        return msgStatus;
    }

    public void setMsgApprovedUserId(Long msgApprovedUserId) 
    {
        this.msgApprovedUserId = msgApprovedUserId;
    }

    public Long getMsgApprovedUserId() 
    {
        return msgApprovedUserId;
    }

    public void setMsgApprovedTime(Date msgApprovedTime) 
    {
        this.msgApprovedTime = msgApprovedTime;
    }

    public Date getMsgApprovedTime() 
    {
        return msgApprovedTime;
    }

    public void setMsgUnapprovedReason(String msgUnapprovedReason) 
    {
        this.msgUnapprovedReason = msgUnapprovedReason;
    }

    public String getMsgUnapprovedReason() 
    {
        return msgUnapprovedReason;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("msgId", getMsgId())
            .append("userId", getUserId())
            .append("userName", getUserName())
            .append("nickName", getNickName())
            .append("phonenumber", getPhonenumber())
            .append("email", getEmail())
            .append("orgId", getOrgId())
            .append("orgName", getOrgName())
            .append("msgContent", getMsgContent())
            .append("msgStatus", getMsgStatus())
            .append("msgApprovedUserId", getMsgApprovedUserId())
            .append("msgApprovedTime", getMsgApprovedTime())
            .append("msgUnapprovedReason", getMsgUnapprovedReason())
            .toString();
    }
}
